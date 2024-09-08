import concrete.numpy as cnp


def save(filter, path_dir):
    """Export all needed artifacts for the client and server interfaces."""

    # Save the circuit for the server
    path_circuit_server = path_dir / "server.zip"
    filter.fhe_circuit.server.save(path_circuit_server)

    # Save the circuit for the client
    path_circuit_client = path_dir / "client.zip"
    filter.fhe_circuit.client.save(path_circuit_client)


# Load the server
server = cnp.Server.load(path_dir / "server.zip")

# Load the client and indicate where to store the private keys
client = cnp.Client.load(path_dir / "client.zip", key_dir)


def encrypt_serialize(client, filter, input_image):
    """Encrypt and serialize the input image in the clear."""

    # Encrypt the image
    encrypted_image = client.encrypt(preprocessed_image)

    # Serialize the encrypted image to be sent to the server
    serialized_encrypted_image = client.specs.serialize_public_args(
        encrypted_image)
    return serialized_encrypted_image


def deserialize_decrypt_post_process(
    client,
    filter,
    serialized_encrypted_output_image
):
    """Deserialize, decrypt and post-process the output image in the clear."""
    # Deserialize the encrypted image
    encrypted_output_image = client.specs.unserialize_public_result(
        serialized_encrypted_output_image
    )

    # Decrypt the image
    output_image = client.decrypt(encrypted_output_image)

    # Post-process the image
    post_processed_output_image = filter.post_processing(output_image)

    return post_processed_output_image


# Generate the keys
client.keygen()

# Retrieve the evaluation keys
client.evaluation_keys.serialize()


def run(server, serialized_encrypted_image, serialized_evaluation_keys):
    """Run the filter on the server over an encrypted image."""

    # Deserialize the encrypted input image and the evaluation keys
    encrypted_image = server.client_specs.unserialize_public_args(
        serialized_encrypted_image
    )
    evaluation_keys = cnp.EvaluationKeys.unserialize(
        serialized_evaluation_keys
    )

    # Execute the filter in FHE
    encrypted_output = server.run(
        encrypted_image, evaluation_keys
    )

    # Serialize the encrypted output image
    serialized_encrypted_output = server.client_specs.serialize_public_result(
        encrypted_output
    )

    return serialized_encrypted_output
