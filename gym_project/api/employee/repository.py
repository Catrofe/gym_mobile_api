from sqlalchemy import select, update
from sqlalchemy.sql.expression import exists

from gym_project.api.employee.models import (
    EmployeeEdit,
    EmployeeForgotPassword,
    EmployeeLogin,
    EmployeeRegister,
)
from gym_project.infra.Entities.entities import (
    Employee,
    PydanticEmployee,
    get_session_maker,
)


class EmployeeRepository:
    def __init__(self) -> None:
        self.sessionmaker = get_session_maker()

    async def employee_is_valid(self, employee: EmployeeRegister) -> bool:
        async with self.sessionmaker() as session:
            query = await session.execute(
                select((exists(Employee))).filter(
                    (Employee.username == employee.username)
                    | (Employee.cpf == employee.cpf)
                    | (Employee.email == employee.email)
                    | (Employee.phoneNumber == employee.phoneNumber)
                )
            )
            return bool(query.scalar())

    async def employee_is_valid_to_edit(self, employee: EmployeeEdit) -> bool:
        async with self.sessionmaker() as session:
            query = await session.execute(
                select((exists(Employee))).filter(
                    (Employee.email == employee.email)
                    | (Employee.phoneNumber == employee.phoneNumber)
                )
            )
            return bool(query.scalar())

    async def register_employee(self, body: EmployeeRegister) -> PydanticEmployee:
        async with self.sessionmaker() as session:
            employee = Employee(**body.dict())
            session.add(employee)
            await session.commit()

        return PydanticEmployee.from_orm(employee)

    async def login_employee(self, employee: EmployeeLogin) -> PydanticEmployee:
        async with self.sessionmaker() as session:
            query = await session.execute(
                select(Employee)
                .where(Employee.isActive)
                .filter(
                    (Employee.username == employee.login)
                    | (Employee.cpf == employee.login)
                    | (Employee.email == employee.login)
                    | (Employee.phoneNumber == employee.login)
                )
            )
        return PydanticEmployee.from_orm(result) if (result := query.scalar()) else None

    async def get_employee(self, id_employee: int) -> PydanticEmployee | None:
        async with self.sessionmaker() as session:
            query = await session.execute(
                select(Employee).filter(Employee.id == id_employee)
            )
            return (
                PydanticEmployee.from_orm(result)
                if (result := query.scalar())
                else None
            )

    async def update_employee(
        self, id_employee: int, employee_request: EmployeeEdit
    ) -> PydanticEmployee:
        async with self.sessionmaker() as session:
            query = await session.execute(
                select(Employee).filter(Employee.id == id_employee)
            )
            result = query.scalar()

            for attr, value in employee_request.dict().items():
                if value:
                    setattr(result, attr, value)

            session.add(result)
            await session.commit()
            return PydanticEmployee.from_orm(result)

    async def verify_if_is_employee(
        self, employee_request: EmployeeForgotPassword
    ) -> bool:
        async with self.sessionmaker() as session:
            query = await session.execute(
                select(exists(Employee)).where(
                    Employee.username == employee_request.username,
                    Employee.email == employee_request.email,
                    Employee.cpf == employee_request.cpf,
                    Employee.phoneNumber == employee_request.phoneNumber,
                    Employee.isActive,
                )
            )
        return bool(query.scalar())

    async def update_password(self, employee_request: EmployeeForgotPassword) -> None:
        async with self.sessionmaker() as session:
            await session.execute(
                update(Employee)
                .where(Employee.email == employee_request.email)
                .values(password=employee_request.password)
            )
            await session.commit()
