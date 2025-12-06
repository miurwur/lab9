# Исходный код декоратора с параметрами.
import sys
from io import StringIO, TextIOWrapper
import logging
import functools
import inspect
from typing import Callable


def logger(*, handle=sys.stdout):  # func deleted for convinience
    match handle:
        case TextIOWrapper() | StringIO() as io:
            writer_out = writer_err = lambda contents: io.write(contents + '\n')

        case logging.Logger() as logger:
            writer_out = logger.info
            writer_err = logger.error
        case _:
            raise Exception("Unsupported handle")

    def wrapper(func: Callable):
        @functools.wraps(func)  # we need to save original naming of functions.
        def _wrapper_impl(*args, **kwargs):
            def get_sign_params():
                signature = inspect.signature(func)
                args_together = signature.bind(*args, **kwargs)
                args_together.apply_defaults()
                return args_together

            params = get_sign_params()
            try:
                writer_out(f"Функция {func.__name__} начала работу с параметрами {params}.")
                res = func(*args, **kwargs)
                writer_out(f"Функция {func.__name__} завершила свою работу с результатом: {res} \n")
                return res
            except Exception as e:
                writer_err(
                    f"!!!ФУНКЦИЯ {func.__name__} ЗАВЕРШИЛА СВОЮ РАБОТУ С ВОТ ЭТОЙ ОШИБКОЙ: {type(e).__name__}. ВОТ ТЕКСТ ЭТОЙ ОШИБКИ: {str(e)} \n")
                raise Exception from e

        return _wrapper_impl

    return wrapper