import numpy as np
from random import shuffle


def svm_loss_naive(W, X, y, reg):
    """
    Structured SVM loss function, naive implementation (with loops).

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    dW = np.zeros(W.shape)  # initialize the gradient as zero

    # compute the loss and the gradient
    C = W.shape[1]
    N = X.shape[0]
    loss = 0.0
    for i in xrange(N):
        scores = X[i].dot(W)
        correct_class_score = scores[y[i]]
        loss_margin = 0
        for j in xrange(C):
            if j == y[i]:
                continue
            margin = scores[j] - correct_class_score + 1  # note delta = 1
            if margin > 0:
                loss_margin += 1
                loss += margin
                dW[:, j] += X[i, :]
        dW[:, y[i]] -= loss_margin * X[i, :]

    # Right now the loss is a sum over all training examples, but we want it
    # to be an average instead so we divide by N.
    loss /= N
    dW /= N

    # Add regularization to the loss.
    loss += 0.5 * reg * np.sum(W * W)
    dW += reg * W

    #############################################################################
    # TODO:                                                                     #
    # Compute the gradient of the loss function and store it dW.                #
    # Rather that first computing the loss and then computing the derivative,   #
    # it may be simpler to compute the derivative at the same time that the     #
    # loss is being computed. As a result you may need to modify some of the    #
    # code above to compute the gradient.                                       #
    #############################################################################


    return loss, dW


def svm_loss_vectorized(W, X, y, reg):
    """
    Structured SVM loss function, vectorized implementation.

    Inputs and outputs are the same as svm_loss_naive.
    """
    loss = 0.0
    dW = np.zeros(W.shape)  # initialize the gradient as zero

    #############################################################################
    # TODO:                                                                     #
    # Implement a vectorized version of the structured SVM loss, storing the    #
    # result in loss.                                                           #
    #############################################################################
    scores = X.dot(W)
    C = W.shape[1]
    N = X.shape[0]
    correct_class_score = scores[np.arange(N),
                                 y[np.arange(N)]].reshape(N, 1)
    margin = np.asarray(scores - correct_class_score + 1)
    margin[margin < 0] = 0
    loss += np.sum(margin) - N
    loss /= N
    loss += 0.5 * reg * np.sum(W * W)
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################


    #############################################################################
    # TODO:                                                                     #
    # Implement a vectorized version of the gradient for the structured SVM     #
    # loss, storing the result in dW.                                           #
    #                                                                           #
    # Hint: Instead of computing the gradient from scratch, it may be easier    #
    # to reuse some of the intermediate values that you used to compute the     #
    # loss.                                                                     #
    #############################################################################

    mask = np.zeros(margin.shape)
    margin[np.arange(N), y[np.arange(N)]] = 0
    minus_sum = np.sum(margin > 0, axis=1)
    mask[margin > 0] = 1
    mask[np.arange(N), y[np.arange(N)]] -= minus_sum

    dW = np.transpose(X).dot(mask)
    dW /= N
    dW += reg * W
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################

    return loss, dW
