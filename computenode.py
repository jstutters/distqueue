from paramiko import SSHClient
from threading import Thread


class ComputeNode(object):
    def __init__(self, hostname, capabilities, port=22):
        self.hostname = hostname
        self.port = port
        self._connected = False
        self._worker_thread = None
        self.last_result = None

    def _connect(self, hostname, port):
        self.hostname = hostname
        self._client = SSHClient()
        self._client.load_system_host_keys()
        self._client.connect(hostname, port)
        t = self._client.get_transport()
        self._channel = t.open_session()
        self._connected = True

    def call_remote_host(self, cmd):
        self._channel.exec_command(cmd)
        exit_status = self._channel.recv_exit_status()
        output = self._channel.makefile('rb', -1).read()
        self.last_result = (exit_status, output)

    def execute(self, cmd):
        if not self._connected:
            self._connect(self.hostname, self.port)
        self._worker_thread = Thread(target=self.call_remote_host, args=(cmd,))
        self._worker_thread.start()

    def is_free(self):
        if self._worker_thread is None:
            return True
        else:
            return not self._worker_thread.is_alive()

    def is_busy(self):
        return not self.is_free()

    def __del__(self):
        if self._connected:
            self._client.close()
