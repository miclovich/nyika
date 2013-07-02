
from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from rapidsms.models import Contact
from .models import Group


class RegisterHandler(KeywordHandler):
    """
    Allow remote users to register themselves, by creating a Contact
    object and associating it with their Connection. For example::

        >>> RegisterHandler.test('join Adam Mckaig')
        ['Thank you for registering, Adam Mckaig!']

        >>> Contact.objects.filter(name="Adam Mckaig")
        [<Contact: Adam Mckaig>]

    Note that the ``name`` field of the Contact model is not constrained
    to be unique, so this handler does not reject duplicate names. If
    you wish to enforce unique usernames or aliases, you must extend
    Contact, disable this handler, and write your own.
    """

    keyword = "register|reg|join"

    def help(self):
        self.respond("To register, send JOIN <NAME>")

    def handle(self, text):
        contact = Contact.objects.create(name=text)
        self.msg.connection.contact = contact

        # telephone number
        connection_identity = self.msg.connection.identity

        # You can process text like this
        # text => "name group"
        text_split = text.split()
        name = text_split[0]
        group_name = text_split[1]
        # or you can process text like this (check docstring)
        """
        # Some suggestions
        text = self.msg.text # returns the same thing
        # working with the Group object
        group = Group.objects.filter(name = group_name)[0]
        # You might need to store this in a new model to join this data to something or to
        # attach numbers to a subscriber for example. Note: this object/table doesn't exist
        subscribers = Subscriber.objects.create(group=group, connection=self.msg.connection)
        """
        self.msg.connection.save()

        self.respond("Thank you for registering, %(name)s!" % {'name': contact.name})
