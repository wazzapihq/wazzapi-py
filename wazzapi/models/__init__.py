from .base import WazzapiModel
from .contacts import *
from .contacts import __all__ as contacts_all
from .devices import *
from .devices import __all__ as devices_all
from .groups import *
from .groups import __all__ as groups_all
from .media import *
from .media import __all__ as media_all
from .messages import *
from .messages import __all__ as messages_all
from .templates import *
from .templates import __all__ as templates_all
from .webhooks import *
from .webhooks import __all__ as webhooks_all

__all__ = [
	"WazzapiModel",
	*contacts_all,
	*devices_all,
	*groups_all,
	*media_all,
	*messages_all,
	*templates_all,
	*webhooks_all,
]