CONST = {
    FOO = 1,
    BAR = 2,
}

a = {
    [CONST.FOO] = function()
        print("foo")
    end,

    [CONST.BAR] = function()
        print("bar")
    end,

    [CONST.FOO] = function()
        print("bar")
    end,
}
