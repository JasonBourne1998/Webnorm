import time
import functools
import logging

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger()


def user(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info(f"\x1b[34;1m[User ]\x1b[0m Start task: {func.__name__}")
            start_time = time.perf_counter()
            passed, code = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            logger.info(f"\x1b[34;1m[User ]\x1b[0m Finished task in {total_time:.4f} seconds")
            logger.info(f"\x1b[34;1m[User ]\x1b[0m Final solution:\n{code}")
            return passed, code
        except Exception as e:
            logger.exception(f"Exception raised in {func.__name__}. exception: {str(e)}")
            raise e
    return wrapper


def agent(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            logger.info(f"\x1b[35;1m[Agent]\x1b[0m Generated response\n{result}")
            return result
        except Exception as e:
            logger.exception(f"Exception raised in {func.__name__}. exception: {str(e)}")
            raise e
    return wrapper


def environment(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            passed, fails, reasons = func(*args, **kwargs)

            if not passed:
                reasons_str = "\n".join([f"\t\x1b[91;1m[{i}]\x1b[0m {reason}" for i, reason in enumerate(reasons)]) if isinstance(reasons, list) else reasons
                logger.info(f"\x1b[36;1m[Env. ]\x1b[0m Finished testing code, \x1b[31;1mfailed {fails} test cases.\x1b[0m\n{reasons_str}")
            else:
                logger.info(f"\x1b[36;1m[Env. ]\x1b[0m Finished testing code, \x1b[32;1mpassed all test cases.\x1b[0m")
                
            return passed, fails, reasons
        except Exception as e:
            logger.exception(f"Exception raised in {func.__name__}. exception: {str(e)}")
            raise e
    return wrapper