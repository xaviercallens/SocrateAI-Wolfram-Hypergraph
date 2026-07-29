import torch
import pytest
from hypergraph.tensor_masking import DifferentiableTopologicalMask, topological_relu


def test_differentiable_topological_mask_forward_train():
    num_nodes = 5
    mask_layer = DifferentiableTopologicalMask(
        num_nodes=num_nodes, threshold=0.5)
    adj = torch.eye(num_nodes)

    mask_layer.train()
    out = mask_layer(adj)
    assert out.shape == (num_nodes, num_nodes)
    assert (out >= 0.0).all() and (out <= 1.0).all()


def test_differentiable_topological_mask_eval():
    num_nodes = 5
    mask_layer = DifferentiableTopologicalMask(
        num_nodes=num_nodes, threshold=0.5)
    adj = torch.eye(num_nodes)

    mask_layer.eval()
    out = mask_layer(adj)
    assert out.shape == (num_nodes, num_nodes)


def test_backward_gradient_flow():
    num_nodes = 4
    mask_layer = DifferentiableTopologicalMask(
        num_nodes=num_nodes, threshold=0.5)
    adj = torch.ones((num_nodes, num_nodes), requires_grad=True)

    mask_layer.train()
    out = mask_layer(adj)
    loss = out.sum()
    loss.backward()

    assert mask_layer.edge_weights.grad is not None
    assert (mask_layer.edge_weights.grad != 0).any()


def test_topological_relu():
    x = torch.tensor([0.2, 0.4, 0.6, 0.8])
    res = topological_relu(x, threshold=0.5)
    expected = torch.tensor([0.0, 0.0, 0.6, 0.8])
    assert torch.allclose(res, expected)
