

@classmethod
def forward(cls, ctx, input, p=0.5, train=False, inplace=False):
    if ((p < 0) or (p > 1)):
        raise ValueError('dropout probability has to be between 0 and 1, but got {}'.format(p))
    ctx.p = p
    ctx.train = train
    ctx.inplace = inplace
    if ((ctx.p == 0) or (not ctx.train)):
        return input
    if ctx.inplace:
        ctx.mark_dirty(input)
        output = input
    else:
        output = input.clone()
    ctx.noise = cls._make_noise(input)
    if (ctx.p == 1):
        ctx.noise.fill_(0)
    else:
        ctx.noise.bernoulli_((1 - ctx.p)).div_((1 - ctx.p))
    ctx.noise = ctx.noise.expand_as(input)
    output.mul_(ctx.noise)
    return output
