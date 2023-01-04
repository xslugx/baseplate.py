#
# Autogenerated by Thrift Compiler (0.17.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py:slots
#
import logging
import sys

from thrift.protocol.TProtocol import TProtocolException
from thrift.Thrift import TApplicationException
from thrift.Thrift import TException
from thrift.Thrift import TFrozenDict
from thrift.Thrift import TMessageType
from thrift.Thrift import TProcessor
from thrift.Thrift import TType
from thrift.transport import TTransport
from thrift.TRecursive import fix_spec

from .ttypes import *

all_structs = []


class Iface(object):
    def put(self, queue_name, max_messages, message, timeout):
        """
        Parameters:
         - queue_name
         - max_messages
         - message
         - timeout

        """
        pass

    def get(self, queue_name, max_messages, timeout):
        """
        Parameters:
         - queue_name
         - max_messages
         - timeout

        """
        pass


class Client(Iface):
    def __init__(self, iprot, oprot=None):
        self._iprot = self._oprot = iprot
        if oprot is not None:
            self._oprot = oprot
        self._seqid = 0

    def put(self, queue_name, max_messages, message, timeout):
        """
        Parameters:
         - queue_name
         - max_messages
         - message
         - timeout

        """
        self.send_put(queue_name, max_messages, message, timeout)
        return self.recv_put()

    def send_put(self, queue_name, max_messages, message, timeout):
        self._oprot.writeMessageBegin("put", TMessageType.CALL, self._seqid)
        args = put_args()
        args.queue_name = queue_name
        args.max_messages = max_messages
        args.message = message
        args.timeout = timeout
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_put(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = put_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.timed_out_error is not None:
            raise result.timed_out_error
        raise TApplicationException(
            TApplicationException.MISSING_RESULT, "put failed: unknown result"
        )

    def get(self, queue_name, max_messages, timeout):
        """
        Parameters:
         - queue_name
         - max_messages
         - timeout

        """
        self.send_get(queue_name, max_messages, timeout)
        return self.recv_get()

    def send_get(self, queue_name, max_messages, timeout):
        self._oprot.writeMessageBegin("get", TMessageType.CALL, self._seqid)
        args = get_args()
        args.queue_name = queue_name
        args.max_messages = max_messages
        args.timeout = timeout
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_get(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = get_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.timed_out_error is not None:
            raise result.timed_out_error
        raise TApplicationException(
            TApplicationException.MISSING_RESULT, "get failed: unknown result"
        )


class Processor(Iface, TProcessor):
    def __init__(self, handler):
        self._handler = handler
        self._processMap = {}
        self._processMap["put"] = Processor.process_put
        self._processMap["get"] = Processor.process_get
        self._on_message_begin = None

    def on_message_begin(self, func):
        self._on_message_begin = func

    def process(self, iprot, oprot):
        (name, type, seqid) = iprot.readMessageBegin()
        if self._on_message_begin:
            self._on_message_begin(name, type, seqid)
        if name not in self._processMap:
            iprot.skip(TType.STRUCT)
            iprot.readMessageEnd()
            x = TApplicationException(
                TApplicationException.UNKNOWN_METHOD, "Unknown function %s" % (name)
            )
            oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
            x.write(oprot)
            oprot.writeMessageEnd()
            oprot.trans.flush()
            return
        else:
            self._processMap[name](self, seqid, iprot, oprot)
        return True

    def process_put(self, seqid, iprot, oprot):
        args = put_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = put_result()
        try:
            result.success = self._handler.put(
                args.queue_name, args.max_messages, args.message, args.timeout
            )
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TimedOutError as timed_out_error:
            msg_type = TMessageType.REPLY
            result.timed_out_error = timed_out_error
        except TApplicationException as ex:
            logging.exception("TApplication exception in handler")
            msg_type = TMessageType.EXCEPTION
            result = ex
        except Exception:
            logging.exception("Unexpected exception in handler")
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, "Internal error")
        oprot.writeMessageBegin("put", msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_get(self, seqid, iprot, oprot):
        args = get_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = get_result()
        try:
            result.success = self._handler.get(args.queue_name, args.max_messages, args.timeout)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TimedOutError as timed_out_error:
            msg_type = TMessageType.REPLY
            result.timed_out_error = timed_out_error
        except TApplicationException as ex:
            logging.exception("TApplication exception in handler")
            msg_type = TMessageType.EXCEPTION
            result = ex
        except Exception:
            logging.exception("Unexpected exception in handler")
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, "Internal error")
        oprot.writeMessageBegin("get", msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()


# HELPER FUNCTIONS AND STRUCTURES


class put_args(object):
    """
    Attributes:
     - queue_name
     - max_messages
     - message
     - timeout

    """

    __slots__ = (
        "queue_name",
        "max_messages",
        "message",
        "timeout",
    )

    def __init__(
        self,
        queue_name=None,
        max_messages=None,
        message=None,
        timeout=None,
    ):
        self.queue_name = queue_name
        self.max_messages = max_messages
        self.message = message
        self.timeout = timeout

    def read(self, iprot):
        if (
            iprot._fast_decode is not None
            and isinstance(iprot.trans, TTransport.CReadableTransport)
            and self.thrift_spec is not None
        ):
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.queue_name = (
                        iprot.readString().decode("utf-8", errors="replace")
                        if sys.version_info[0] == 2
                        else iprot.readString()
                    )
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I64:
                    self.max_messages = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.message = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.DOUBLE:
                    self.timeout = iprot.readDouble()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin("put_args")
        if self.queue_name is not None:
            oprot.writeFieldBegin("queue_name", TType.STRING, 1)
            oprot.writeString(
                self.queue_name.encode("utf-8") if sys.version_info[0] == 2 else self.queue_name
            )
            oprot.writeFieldEnd()
        if self.max_messages is not None:
            oprot.writeFieldBegin("max_messages", TType.I64, 2)
            oprot.writeI64(self.max_messages)
            oprot.writeFieldEnd()
        if self.message is not None:
            oprot.writeFieldBegin("message", TType.STRING, 3)
            oprot.writeBinary(self.message)
            oprot.writeFieldEnd()
        if self.timeout is not None:
            oprot.writeFieldBegin("timeout", TType.DOUBLE, 4)
            oprot.writeDouble(self.timeout)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ["%s=%r" % (key, getattr(self, key)) for key in self.__slots__]
        return "%s(%s)" % (self.__class__.__name__, ", ".join(L))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for attr in self.__slots__:
            my_val = getattr(self, attr)
            other_val = getattr(other, attr)
            if my_val != other_val:
                return False
        return True

    def __ne__(self, other):
        return not (self == other)


all_structs.append(put_args)
put_args.thrift_spec = (
    None,  # 0
    (
        1,
        TType.STRING,
        "queue_name",
        "UTF8",
        None,
    ),  # 1
    (
        2,
        TType.I64,
        "max_messages",
        None,
        None,
    ),  # 2
    (
        3,
        TType.STRING,
        "message",
        "BINARY",
        None,
    ),  # 3
    (
        4,
        TType.DOUBLE,
        "timeout",
        None,
        None,
    ),  # 4
)


class put_result(object):
    """
    Attributes:
     - success
     - timed_out_error

    """

    __slots__ = (
        "success",
        "timed_out_error",
    )

    def __init__(
        self,
        success=None,
        timed_out_error=None,
    ):
        self.success = success
        self.timed_out_error = timed_out_error

    def read(self, iprot):
        if (
            iprot._fast_decode is not None
            and isinstance(iprot.trans, TTransport.CReadableTransport)
            and self.thrift_spec is not None
        ):
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = PutResponse()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.timed_out_error = TimedOutError.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin("put_result")
        if self.success is not None:
            oprot.writeFieldBegin("success", TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.timed_out_error is not None:
            oprot.writeFieldBegin("timed_out_error", TType.STRUCT, 1)
            self.timed_out_error.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ["%s=%r" % (key, getattr(self, key)) for key in self.__slots__]
        return "%s(%s)" % (self.__class__.__name__, ", ".join(L))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for attr in self.__slots__:
            my_val = getattr(self, attr)
            other_val = getattr(other, attr)
            if my_val != other_val:
                return False
        return True

    def __ne__(self, other):
        return not (self == other)


all_structs.append(put_result)
put_result.thrift_spec = (
    (
        0,
        TType.STRUCT,
        "success",
        [PutResponse, None],
        None,
    ),  # 0
    (
        1,
        TType.STRUCT,
        "timed_out_error",
        [TimedOutError, None],
        None,
    ),  # 1
)


class get_args(object):
    """
    Attributes:
     - queue_name
     - max_messages
     - timeout

    """

    __slots__ = (
        "queue_name",
        "max_messages",
        "timeout",
    )

    def __init__(
        self,
        queue_name=None,
        max_messages=None,
        timeout=None,
    ):
        self.queue_name = queue_name
        self.max_messages = max_messages
        self.timeout = timeout

    def read(self, iprot):
        if (
            iprot._fast_decode is not None
            and isinstance(iprot.trans, TTransport.CReadableTransport)
            and self.thrift_spec is not None
        ):
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.queue_name = (
                        iprot.readString().decode("utf-8", errors="replace")
                        if sys.version_info[0] == 2
                        else iprot.readString()
                    )
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I64:
                    self.max_messages = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.DOUBLE:
                    self.timeout = iprot.readDouble()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin("get_args")
        if self.queue_name is not None:
            oprot.writeFieldBegin("queue_name", TType.STRING, 1)
            oprot.writeString(
                self.queue_name.encode("utf-8") if sys.version_info[0] == 2 else self.queue_name
            )
            oprot.writeFieldEnd()
        if self.max_messages is not None:
            oprot.writeFieldBegin("max_messages", TType.I64, 2)
            oprot.writeI64(self.max_messages)
            oprot.writeFieldEnd()
        if self.timeout is not None:
            oprot.writeFieldBegin("timeout", TType.DOUBLE, 3)
            oprot.writeDouble(self.timeout)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ["%s=%r" % (key, getattr(self, key)) for key in self.__slots__]
        return "%s(%s)" % (self.__class__.__name__, ", ".join(L))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for attr in self.__slots__:
            my_val = getattr(self, attr)
            other_val = getattr(other, attr)
            if my_val != other_val:
                return False
        return True

    def __ne__(self, other):
        return not (self == other)


all_structs.append(get_args)
get_args.thrift_spec = (
    None,  # 0
    (
        1,
        TType.STRING,
        "queue_name",
        "UTF8",
        None,
    ),  # 1
    (
        2,
        TType.I64,
        "max_messages",
        None,
        None,
    ),  # 2
    (
        3,
        TType.DOUBLE,
        "timeout",
        None,
        None,
    ),  # 3
)


class get_result(object):
    """
    Attributes:
     - success
     - timed_out_error

    """

    __slots__ = (
        "success",
        "timed_out_error",
    )

    def __init__(
        self,
        success=None,
        timed_out_error=None,
    ):
        self.success = success
        self.timed_out_error = timed_out_error

    def read(self, iprot):
        if (
            iprot._fast_decode is not None
            and isinstance(iprot.trans, TTransport.CReadableTransport)
            and self.thrift_spec is not None
        ):
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = GetResponse()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.timed_out_error = TimedOutError.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin("get_result")
        if self.success is not None:
            oprot.writeFieldBegin("success", TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.timed_out_error is not None:
            oprot.writeFieldBegin("timed_out_error", TType.STRUCT, 1)
            self.timed_out_error.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ["%s=%r" % (key, getattr(self, key)) for key in self.__slots__]
        return "%s(%s)" % (self.__class__.__name__, ", ".join(L))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for attr in self.__slots__:
            my_val = getattr(self, attr)
            other_val = getattr(other, attr)
            if my_val != other_val:
                return False
        return True

    def __ne__(self, other):
        return not (self == other)


all_structs.append(get_result)
get_result.thrift_spec = (
    (
        0,
        TType.STRUCT,
        "success",
        [GetResponse, None],
        None,
    ),  # 0
    (
        1,
        TType.STRUCT,
        "timed_out_error",
        [TimedOutError, None],
        None,
    ),  # 1
)
fix_spec(all_structs)
del all_structs
