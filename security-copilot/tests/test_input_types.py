from config.input_types import INPUT_TYPES, describe_input


def test_sample_inputs_are_registered():
    assert len(INPUT_TYPES) == 21
    assert describe_input("terraform")["category"] == "infrastructure"
    assert describe_input("docker_image")["value_kind"] == "image_reference"

