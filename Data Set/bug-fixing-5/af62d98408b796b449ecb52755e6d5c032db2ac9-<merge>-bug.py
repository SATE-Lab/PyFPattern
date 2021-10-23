def merge(self, model, destination, sources, timestamp=None, environment_ids=None):
    environment_ids = (set(environment_ids) if (environment_ids is not None) else set()).union([None])
    self.validate_arguments([model], environment_ids)
    for environment_id in environment_ids:
        destination = self.data[model][(destination, environment_id)]
        for source in sources:
            for (bucket, count) in self.data[model].pop((source, environment_id), {
                
            }).items():
                destination[bucket] += count