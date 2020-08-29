window.app.controller('MultiLabelController', function ($scope, $http) {
    $scope.labels = ["TP", "TN", "FP", "FN", "accuracy", "precision", "recall", "f1"];
    $scope.filterLabel = "";
    $scope.filterExpectedClass = true;
    $scope.filterActualClass = true;
    $scope.toggleItem = function (row, index) {
        $scope.filterIndex = index;
        $scope.filterLabel = row["label"];
        if (index == 0) {
            $scope.filterActualClass = true;
            $scope.filterExpectedClass = true;
        }
        if (index == 1) {
            $scope.filterActualClass = false;
            $scope.filterExpectedClass = false;
        }
        if (index == 2) {
            $scope.filterActualClass = true;
            $scope.filterExpectedClass = false;
        }
        if (index == 3) {
            $scope.filterActualClass = false;
            $scope.filterExpectedClass = true;
        }
//            $scope.$apply();
    };

    $scope.isFocusItem = function (row, index) {
        return $scope.filterIndex == index && $scope.filterLabel == row["label"];
    };
    $scope.filter = function (text) {
        return _.filter(text, function (item) {
            var expectedClass = _.contains(item["expected"], $scope.filterLabel);
            var actualClass = _.contains(item["actual"], $scope.filterLabel);
            return expectedClass == $scope.filterExpectedClass && actualClass == $scope.filterActualClass;
        });
    };
    $http.get("multilabel.json")
        .then(function (result) {
            var data = result["data"];
            var text = [];
            for (var i = 0; i < data["X_test"].length; i++) {
                text.push({
                    "content": data["X_test"][i],
                    "expected": data["y_test"][i],
                    "actual": data["y_pred"][i]

                })
            }
            $scope.text = text;
            $scope.score = _.map(data["score"], function (v, i) {
                return {
                    "label": i,
                    "scores": _.chain(v).map(function (value, name) {
                        return {
                            "name": name,
                            "value": value
                        }
                    }).sortBy(function (item) {
                        return $scope.labels.indexOf(item["name"])
                    }).map(function (item) {
                        return item["value"];
                    }).value()
                }
            });
            $scope.score = _.sortBy($scope.score, function (item) {
                return item.label;
            });
            console.log($scope.score);
        });
});
