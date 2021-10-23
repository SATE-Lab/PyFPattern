def init_data_type_with_fusion(self, input_dt, fuse_relu, fuse_residual):
    self.srctype = input_dt
    self.dsttype = (np.uint8 if fuse_relu else np.int8)

    def init_fuse_relu(self):
        self.fuse_relu = fuse_relu

    def init_fuse_residual(self):
        self.fuse_residual = fuse_residual