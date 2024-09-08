def forward(self, x):
    """Forward pass with a single convolution using a 2D kernel."""
    kernel = self.kernel.expand(
        self.n_out_channels,
        self.n_in_channels // self.groups,
        self.kernel.shape[0],
        self.kernel.shape[1],
    )

    # Reshape the input to (1, 3, Height, Width)
    x = x.transpose(2, 0).unsqueeze(axis=0)

    # Apply the convolution
    x = nn.functional.conv2d(
        x,
        kernel,
        stride=stride,
        groups=self.groups
    )

    # Reshape the output to (Height, Width, 3)
    x = x.transpose(1, 3).reshape((
        x.shape[2],
        x.shape[3],
        self.n_out_channel
    ))

    return x


kernel = [
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0],
]

sharpen_filter = TorchConv(kernel, n_out_channels=3, groups=3)


class TorchInverted(nn.Module):
    """Torch inverted model."""

    def forward(self, x):
        """Forward pass for inverting an image's colors."""
        return 255 - x


def post_processing(output_image):
    """Apply post-processing to the encrypted output images."""

    output_image = output_image.clip(0, 255)
    return output_image


def post_processing(output_image):
    """Apply post-processing to the encrypted output images."""

    output_image = output_image.clip(0, 255)
    return output_image


INPUT_SHAPE = (100, 100, 3)


# Generate the input set
inputset = tuple(
    numpy.random.randint(
        0,
        256,
        size=INPUT_SHAPE,
        dtype=numpy.int64,
    ) for _ in range(100)
)

# Convert the Torch module to the Numpy module
numpy_module = NumpyModule(
    sharpen_filter,
    dummy_input=torch.from_numpy(inputset[0]),
)

numpy_filter_proxy, parameters_mapping = generate_proxy_function(
    numpy_module.numpy_forward,
    ["inputs"]
)

# Compile the module and retrieve the FHE circuit
compiler = Compiler(
    numpy_filter_proxy,
    {parameters_mapping["inputs"]: "encrypted"},
)
fhe_circuit = compiler.compile(inputset)
