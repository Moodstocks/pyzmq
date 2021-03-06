'''
The decorators module for ``zmq.sugar``.
'''

__all__ = (
    'context',
    'socket'
)


import zmq

from functools import partial
from zmq.decorators.base import ZDecoratorBase


def context(*args, **kwargs):
    '''
    .. versionadded:: 15.3

    :param str name: the keyword argument passed to decorated function
    '''
    return ZDecoratorBase(zmq.Context)(*args, **kwargs)


def socket(*args, **kwargs):
    '''
    .. versionadded:: 15.3

    :param str name: the keyword argument passed to decorated function
    :param str context_name: the keyword only argument to identify context
                             object
    '''
    return _SocketDecorator(zmq.Socket)(*args, **kwargs)


class _SocketDecorator(ZDecoratorBase):

    def hook_preinit(self):
        self.context_name = self.dec_kwargs.pop('context_name', 'context')
        self.context = self._get_context()
        self.target = partial(zmq.Socket, self.context)

    def _get_context(self):
        '''
        Find the ``zmq.Context`` from ``self.wrap_args`` and ``wrap_kwargs``

        First, if there is an keyword argument named ``context`` and it is a
        ``zmq.Context`` instance , we will take it.

        Second, we check all the ``wrap_args``, take the first ``zmq.Context``
        instance.

        Finally, we will provide default Context -- ``zmq.Context.instance``

        :return: a ``zmq.Context`` instance
        '''
        if self.context_name in self.wrap_kwargs:
            ctx = self.wrap_kwargs[self.context_name]

            if isinstance(ctx, zmq.Context):
                return ctx

        for arg in self.wrap_args:
            if not isinstance(arg, zmq.Context):
                continue
            return arg

        return zmq.Context.instance()
