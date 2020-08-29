window.app.controller('ResultController', function ($scope, $http) {

    $scope.isFocusItem = function (row, index) {
        return $scope.filterIndex == index && $scope.filterLabel == row["label"];
    };
    $scope.filter = function (text) {
        return _.filter(text, function (item) {
            var expectedClass = item["expected"] == $scope.filterLabel;
            var actualClass = item["actual"] == $scope.filterLabel;
            return expectedClass == $scope.filterExpectedClass && actualClass == $scope.filterActualClass;
        });
    };

    $http.get("result.json")
        .then(function (result) {

            var data = result["data"];
            data = _.map(data, function (value, key) {
                return {"key": key, "value": value}
            });
            data = _.sortBy(data, function (item) {
                var keys = ["Sample", "Accuracy", "F1 Micro", "F1 Macro", "F1 Weighted"];
                return keys.indexOf(item["key"]);
            });
            $scope.data = data;
        });
});
