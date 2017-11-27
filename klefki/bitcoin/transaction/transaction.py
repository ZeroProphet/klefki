class Transaction:
    def __init__(
            self,
            inputs: list,
            outputs,
            lock_time,
            version=1,
    ):
        self.version = version
        self.in_count = len(inputs)
        self.inputs = inputs
        self.out_count = len(outputs)
        self.outputs = outputs
