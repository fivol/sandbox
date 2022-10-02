import docker
client = docker.from_env()


config = '''
input {
    stdin {}
    generator {
        lines => [
              "line 1",
              "line 2",
              "line 3"
        ]
        count => 3
    }
}
    
output {
    stdout {}
}

'''


class LogstashConfigTestingMachine:
    def __init__(self):
        pass

    def get_running_logstash(self):
        pass

    def set_config(self):
        pass

    def send_text(self) -> str:
        pass


class LogstashTester:
    def __init__(self):
        pass

    def run_test(self):
        pass

    def read_tests(self):
        pass

    def run_all_tests(self):
        pass

# container = client.containers.run('docker.elastic.co/logstash/logstash:7.17.0', detach=True, auto_remove=True)
print(client.containers.list()[0].image)
# print(container.logs())

if __name__ == '__main__':
    path = 'tests/files'
    tester = LogstashTester()
    tester.run_all_tests()
