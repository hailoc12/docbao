from sklearn import linear_model


class SGDClassifier(linear_model.SGDClassifier):
    r"""
    Linear classifiers (SVM, logistic regression, a.o.) with SGD training.

    This estimator implements regularized linear models with stochastic gradient descent (SGD) learning: the gradient of the loss is estimated each sample at a time and the model is updated along the way with a decreasing strength schedule (aka learning rate). SGD allows minibatch (online/out-of-core) learning, see the partial_fit method. For best results using the default learning rate schedule, the data should have zero mean and unit variance.

    This implementation works with data represented as dense or sparse arrays of floating point values for the features. The model it fits can be controlled with the loss parameter; by default, it fits a linear support vector machine (SVM).

    The regularizer is a penalty added to the loss function that shrinks model parameters towards the zero vector using either the squared euclidean norm L2 or the absolute norm L1 or a combination of both (Elastic Net). If the parameter update crosses the 0.0 value because of the regularizer, the update is truncated to 0.0 to allow for learning sparse models and achieve online feature selection.
    """

    def __init__(self, *args, **kwargs):
        # fix FutureWarning when both tol and max_iter is not set
        if 'tol' not in kwargs and 'max_iter' not in kwargs:
            kwargs['tol'] = 1e-3
        super(SGDClassifier, self).__init__(*args, **kwargs)

    def fit(self, X, y, coef_init=None, intercept_init=None,
            sample_weight=None):
        """Fit linear model with Stochastic Gradient Descent.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            Training data

        y : numpy array, shape (n_samples,)
            Target values

        coef_init : array, shape (n_classes, n_features)
            The initial coefficients to warm-start the optimization.

        intercept_init : array, shape (n_classes,)
            The initial intercept to warm-start the optimization.

        sample_weight : array-like, shape (n_samples,), optional
            Weights applied to individual samples.
            If not provided, uniform weights are assumed. These weights will
            be multiplied with class_weight (passed through the
            constructor) if class_weight is specified

        Returns
        -------
        self : returns an instance of self.
        """
        super(SGDClassifier, self).fit(X, y, coef_init, intercept_init,
                                       sample_weight)

    def predict(self, X):
        """Predict class labels for samples in X.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = [n_samples, n_features]
            Samples.

        Returns
        -------
        C : array, shape = [n_samples]
            Predicted class label per sample.
        """
        super(SGDClassifier, self).predict(X)
