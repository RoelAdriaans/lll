import abc

from trainlocationeventsource.domain import NStreinpositie, TreinMaterieelDeel


class AbstractRepository(abc.ABC):
    """Repository that will be used to store and retrieve the Domain to the database"""

    @abc.abstractmethod
    def save(self, positie: NStreinpositie):
        # As for naming, maybe `save`?
        # esdbclient calls it `append_to_stream`. But the question is, are we going to
        # use esdb? And, do we want to have the terminology of the database structure
        # exposed here, or are we abstracting this detail away?
        # Maybe an even better name is `save_update`, since we are saving a position
        # update. Or `save_treinpositie`, since this makes what we are saving explicit.
        #
        # There are 2 hard problems in computer science:
        # cache invalidation, naming things, and off-by-1 errors.
        raise NotImplementedError


class EventStoreDBRepository(AbstractRepository):
    """Store the domain to the EvenstoreDB"""

    def __init__(self):
        # @TODO Please implement me :)
        raise NotImplementedError

    def save(self, positie: NStreinpositie):
        # @TODO Please implement me :)
        raise NotImplementedError
