from taipan_assistant.contacts.record.address import Address
from taipan_assistant.contacts.record.birthday import Birthday
from taipan_assistant.contacts.record.email import Email
from taipan_assistant.contacts.record.name import Name
from taipan_assistant.contacts.record.phone import Phone, PhoneCollection


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = PhoneCollection()
        self.birthday = None
        self.emails = []
        self.address = None

    def add_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return

        self.phones.append(Phone(phone))

    def set_address(self, address: str):
        self.address = Address(address)

    def add_email(self, email: str, is_primary: bool):
        if not self.__can_update_primary_email(email, is_primary):
            raise ValueError("If a contact has an email address, there must be one primary email address")

        # if new is primary set all existed emails as secondary
        if is_primary:
            self.__set_all_emails_as_secondary()

        # if email already there is - update primary status
        for e in self.emails:
            if e.value == email:
                e.primary = is_primary

                return

        if len(self.emails) == 0:
            is_primary = True

        self.emails.append(Email(email, is_primary))

    def change_email(self, old_email: str, new_email: str, is_primary: bool):
        if not self.__can_update_primary_email(old_email, is_primary):
            raise ValueError("If a contact has an email address, there must be one primary email address")

        email = self.find_email(old_email)

        # if new is primary set all existed emails as secondary
        if is_primary:
            self.__set_all_emails_as_secondary()

        email.value = new_email
        email.primary = is_primary

    def __can_update_primary_email(self, email_for_update: str, new_primary_val: bool) -> bool:
        if new_primary_val:
            return True

        # We can`t change primary to not primary, because primary mail is required
        for e in self.emails:
            if e.value == email_for_update and e.primary:
                return False

        return True

    def __set_all_emails_as_secondary(self):
        for e in self.emails:
            e.primary = False

    def find_email(self, email: str) -> Email:
        for e in self.emails:
            if e.value == email:
                return e

        raise ValueError(f'Email {email} does not belong record {self.name}')

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone: str):
        phone_field = Phone(phone)
        if phone_field not in self.phones:
            raise ValueError(f'Phone number {phone} does not belong record {self.name}')

        self.phones.remove(phone_field)

    def edit_phone(self, old_phone: str, new_phone: str):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break

    def find_phone(self, phone: str) -> Phone:
        for phone_field in self.phones:
            if phone_field.value == phone:
                return phone_field

        raise ValueError(f'Phone number {phone} does not belong record {self.name}')

    def __str__(self) -> str:
        result_str = (
            f"Contact name: {self.name.value}, "
            f"phones: {'; '.join(p.value for p in self.phones)}"
        )

        if len(self.emails) > 0:
            result_str = result_str + f", emails: {'; '.join(str(e) for e in self.emails)}"

        if self.address is not None:
            result_str = result_str + f", address: {self.address.value}"

        if self.birthday is not None:
            result_str = result_str + f", birthday: {self.birthday}"

        return result_str
