########
# Copyright (c) 2015 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.


class Event(object):

    def __init__(self, event):
        self._event = event

    def __str__(self):
        deployment_id = self.deployment_id
        timestamp = self.timestamp
        event_type_indicator = self.event_type_indicator
        message = self.text
        info = self.get_operation_info()

        return '{0} {1} {2} {3}{4}'.format(timestamp,
                                           event_type_indicator,
                                           deployment_id,
                                           info,
                                           message)

    def get_operation_info(self):
        operation = self.operation
        node_id = self.node_id
        source_id = self.source_id
        target_id = self.target_id

        context = self._event['context']
        group = context.get('group')
        policy = context.get('policy')
        trigger = context.get('trigger')

        if source_id is not None:
            info = '{0}->{1}|{2}'.format(source_id, target_id, operation)
        else:
            info_elements = [
                e for e in [node_id, operation, group, policy, trigger]
                if e is not None]
            info = '.'.join(info_elements)
        if info:
            info = '[{0}] '.format(info)
        return info

    @property
    def text(self):
        message = self._event['message']['text'].encode('utf-8')
        if self.is_log_message:
            message = '{0}: {1}'.format(self.log_level, message)
        return message

    @property
    def timestamp(self):
        return (self._event.get('@timestamp') or self._event['timestamp'])\
            .split('.')[0]

    @property
    def log_level(self):
        return self._event['level'].upper()

    @property
    def event_type_indicator(self):
        return 'LOG' if self.is_log_message else 'CFY'

    @property
    def operation(self):
        op = self._event['context'].get('operation')
        if op is None:
            return None
        return op.split('.')[-1]

    @property
    def node_id(self):
        return self._event['context'].get('node_id')

    @property
    def source_id(self):
        return self._event['context'].get('source_id')

    @property
    def target_id(self):
        return self._event['context'].get('target_id')

    @property
    def deployment_id(self):
        return '<{0}>'.format(self._event['context']['deployment_id'])

    @property
    def event_type(self):
        return self._event.get('event_type')  # not available for logs

    @property
    def is_log_message(self):
        return 'cloudify_log' in self._event['type']
