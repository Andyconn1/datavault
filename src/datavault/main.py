from datetime import datetime

from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Category(Base):
    """A category of service, cost etc

    e.g. Car, House, Holiday House.
    """

    __tablename__ = "Category"

    key: Mapped[int] = mapped_column(
        primary_key=True, index=True, autoincrement=True, nullable=False
    )
    category: Mapped[str] = mapped_column(nullable=False)


class ServiceType(Base):
    """The type of service being supplied.

    e.g. Mortgage, Gas, Electricity, Car Insurance.
    """

    __tablename__ = "ServiceType"

    key: Mapped[int] = mapped_column(
        primary_key=True, index=True, autoincrement=True, nullable=False
    )
    service_type: Mapped[str] = mapped_column(nullable=False)


class Service(Base):
    __tablename__ = "Service"

    key: Mapped[int] = mapped_column(
        primary_key=True, index=True, autoincrement=True, nullable=False
    )

    # Slowly Changing Dimension
    valid_from: Mapped[datetime] = mapped_column(nullable=False)
    valid_to: Mapped[datetime] = mapped_column(nullable=False)
    is_current: Mapped[bool] = mapped_column(nullable=False, default=False)

    # Review
    prompt_review_date: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime(2100, 1, 1)
    )
    prompt_review_note: Mapped[str] = mapped_column(nullable=False, default="")

    # Service Type
    f_key_service_type: Mapped[int] = mapped_column(
        ForeignKey("ServiceType.key"), nullable=False
    )
    service_type = relationship("ServiceType")

    # Category
    f_key_category: Mapped[int] = mapped_column(
        ForeignKey("Category.key"), nullable=False
    )
    category = relationship("Category")

    # Other
    company_name: Mapped[str] = mapped_column(nullable=False)
    website: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return (
            f"<Service(company_name={self.company_name}, is_current={self.is_current})>"
        )


# Example usage
if __name__ == "__main__":

    # Set up the database
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)

    with Session(engine) as session:

        # Add a category and service type, then commit
        category = Category(category="House")
        session.add(category)

        service_type = ServiceType(service_type="Gas & Electricity")
        session.add(service_type)

        session.commit()  # Commit to save category and service type

        # Now add a service
        service = Service(
            valid_from=datetime(2024, 10, 31),
            valid_to=datetime(2100, 1, 1),
            is_current=True,
            prompt_review_date=datetime(2024, 11, 5),
            prompt_review_note="here's a prompt!",
            f_key_service_type=service_type.key,  # Assign the foreign key
            f_key_category=category.key,  # Assign the foreign key
            company_name="British Gas",
            website="www.bg.com",
            username="andy",
            password="my_pass",
            description="something interesting",
        )
        session.add(service)  # Add the service to the session

        session.commit()  # Commit changes to the database

        # Query all services
        services = session.query(Service).all()
        for service in services:
            print(service)
