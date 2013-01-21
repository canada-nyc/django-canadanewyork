import os

try:
    import heroku
except ImportError:
    pass


class Worker(object):
    app_name = os.environ.get('heroku_app_name')

    @property
    def cloud(self):
        return heroku.from_key(os.environ['HEROKU_API_KEY'])

    @property
    def app(self):
        return self.cloud.apps[self.app_name]

    @property
    def worker_process(self):
        return self.app.processes['worker']

    @property
    def number_workers(self):
        try:
            self.worker_process
        except KeyError:
            return 0
        else:
            return len(self.worker_process._items)

    def scale(self, number):
        print('Scaling heroku worker')
        number = int(number)
        if number != self.number_workers:
            if self.number_workers:
                self.worker_process.scale(number)
            else:
                self.app.processes.add('worker', number)
        else:
            print('Already {} running'.format(number))

    def start(self):
        self.scale(1)

    def stop(self):
        self.scale(0)
