from src.core import member
from datetime import datetime

def run():
    # Add data by default

    member1 = member.create_member(
        first_name="Nico",
        last_name="Barone",
        personal_id_type=1, 
        personal_id="11111111", 
        gender="M",
        member_number=1,
        address="Mi casa", 
        membership_state=True,
        phone_number="12312321", 
        email="nicob@gmail.com",
        activation_date=datetime.now()
    )

    member2 = member.create_member(
        first_name="David",
        last_name="Franco",
        personal_id_type=1, 
        personal_id="222222222", 
        gender="M",
        member_number=2,
        address="Su casa", 
        membership_state=True,
        phone_number="12312321", 
        email="dafran@gmail.com",
        activation_date=datetime.now()
    )

    member3 = member.create_member(
        first_name="Pato",
        last_name="Pato",
        personal_id_type=1, 
        personal_id="33333333", 
        gender="M",
        member_number=3,
        address="Su casa", 
        membership_state=True,
        phone_number="12312321", 
        email="pato@gmail.com",
        activation_date=datetime.now()
    )

    member4 = member.create_member(
        first_name="Thomy",
        last_name="Ruso",
        personal_id_type=1, 
        personal_id="44444444", 
        gender="M",
        member_number=4,
        address="Su casa", 
        membership_state=True,
        phone_number="12312321", 
        email="thomy@gmail.com",
        activation_date=datetime.now()
    )
