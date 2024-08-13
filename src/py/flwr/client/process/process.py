# Copyright 2024 Flower Labs GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Flower background ClientApp."""

from logging import DEBUG, ERROR, INFO

import grpc

from flwr.client.client_app import ClientApp
from flwr.common import Context, Message
from flwr.common.grpc import create_channel
from flwr.common.logger import log
from flwr.common.serde import (
    context_from_proto,
    context_to_proto,
    message_from_proto,
    message_to_proto,
    run_from_proto,
)
from flwr.common.typing import Run

# pylint: disable=E0401,E0611
from flwr.proto.clientappio_pb2 import (
    PullClientAppInputsRequest,
    PullClientAppInputsResponse,
    PushClientAppOutputsRequest,
    PushClientAppOutputsResponse,
)
from flwr.proto.clientappio_pb2_grpc import ClientAppIoStub

from .utils import _get_load_client_app_fn


def _run_background_client(  # pylint: disable=R0914
    address: str,
    token: int,
) -> None:
    """Run background Flower ClientApp process.

    Parameters
    ----------
    address : str
        Address of SuperNode
    token : int
        Unique SuperNode token for ClientApp-SuperNode authentication
    """

    def on_channel_state_change(channel_connectivity: str) -> None:
        """Log channel connectivity."""
        log(DEBUG, channel_connectivity)

    channel = create_channel(
        server_address=address,
        insecure=True,
    )
    channel.subscribe(on_channel_state_change)

    try:
        stub = ClientAppIoStub(channel)

        # Pull Message, Context, and Run from SuperNode
        run, message, context = pull_message(stub=stub, token=token)

        load_client_app_fn = _get_load_client_app_fn(
            default_app_ref="",
            app_path=None,
            multi_app=True,
            flwr_dir=None,
        )

        # Load ClientApp
        client_app: ClientApp = load_client_app_fn(run.fab_id, run.fab_version)

        # Execute ClientApp
        reply_message = client_app(message=message, context=context)

        # Push Message and Context to SuperNode
        _ = push_message(token=token, message=reply_message, context=context, stub=stub)
    except KeyboardInterrupt:
        log(INFO, "Closing connection")
    except grpc.RpcError as e:
        log(ERROR, "GRPC error occurred: %s", str(e))
    finally:
        channel.close()


def pull_message(stub: grpc.Channel, token: int) -> tuple[Run, Message, Context]:
    """Pull message from SuperNode to ClientApp."""
    res: PullClientAppInputsResponse = stub.PullClientAppInputs(
        PullClientAppInputsRequest(token=token)
    )
    run = run_from_proto(res.run)
    message = message_from_proto(res.message)
    context = context_from_proto(res.context)
    return run, message, context


def push_message(
    stub: grpc.Channel, token: int, message: Message, context: Context
) -> PushClientAppOutputsResponse:
    """Push message to SuperNode from ClientApp."""
    proto_message = message_to_proto(message)
    proto_context = context_to_proto(context)
    res: PushClientAppOutputsResponse = stub.PushClientAppOutputs(
        PushClientAppOutputsRequest(
            token=token, message=proto_message, context=proto_context
        )
    )
    return res
