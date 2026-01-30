from flask_sqlalchemy import SQLAlchemy #importa la librería SQLAlchemy para que Flask conecte 
#con una base de datos.
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column #esto es para declarar columnas en SQLAlchemy versión 2.0.
from eralchemy2 import render_er #para cambiar el diagrama porque no aparecía más que el de base

db = SQLAlchemy() #para conectar con el appy gestionar la base de datos

#En caso de que la tabla se llame diferente el nombre de la clase colocar >>" __tablename__ = 'users'"

# TABLA INTERMEDIA PARA NO GENERAR OTRO MODELO
favorites_table = db.Table(
    "favorites_table",
    db.Model.metadata,
    Column("user_id", ForeignKey("users.id"),primary_key=True),
    Column("character_id", ForeignKey("characters.id"), primary_key=True)
)




class User(db.Model): #representa mi tabla user de mi base de datos
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False) #yo he agregado esto como en el ejemplo
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self): #método    
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):#representa mi tabla personajes de mi base de datos
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False) 
    quote: Mapped[str]


    favorite_by: Mapped[list["User"]] = relationship(
        "User",
        secondary=favorites_table,
        back_populates="favorites"
    )
    
    def serialize(self): #método    
        return {

            "id": self.id,
            "name": self.name,
            "quote": self.quote,
            "favorite_by":[user.id for user in self.favorite_by]

        }
    

class Location(db.Model):#representa mi tabla Lugares de mi base de datos
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    quote: Mapped[str]

    favorite_by: Mapped[list["User"]] = relationship(
        "User",
        secondary=favorites_table,
        back_populates="favorites"
#     )
    
#     def serialize(self): #método    
#         return {

#             "id": self.id,
#             "name": self.name,
#             "quote": self.quote,
#             "favorite_by":[user.id for user in self.favorite_by]

#         }




# render_er(db.Model.metadata, 'diagram.png')