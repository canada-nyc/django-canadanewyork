from compressor.filters import CompilerFilter


class UglifyJSFilter(CompilerFilter):
    command = "uglifyjs"
