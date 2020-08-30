window.app.controller('TfidfController', function ($scope, $http) {

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
    $scope.featureOption = "sampleFeatures";
    $scope.$watch('featureOption', function () {
        if ($scope.featureOption == 'sampleFeatures') {
            try {
                $scope.features = $scope.allFeatures.slice(0, 200);
            } catch (e) {
            }
        } else {
            $scope.features = $scope.allFeatures.slice(0, 2000);
        }
    });
    $http.get("tfidf.json")
        .then(function (result) {
            var features = result["data"];
            $scope.numberFeatures = features.length;

            function createTfidfTooltip(feature) {
                return "<div class='point-tooltip'>" +
                    feature["token"] + " " +
                    "(" +
                    "period: " + feature["period"] + ", " +
                    "df: " + feature["df"].toFixed(5) + ", " +
                    "idf: " + feature["idf"].toFixed(4) +
                    ")</div>";
            }

            var series = _.map(features, function (feature) {
                var random_ngram = feature["ngram"] - Math.random();
                return {
                    "name": feature["token"],
                    "value": [feature["idf"], random_ngram],
                    "tooltip": createTfidfTooltip(feature)
                }
            });
            draw(series);
        });

    function draw(data) {
        var margin = {top: 20, right: 15, bottom: 60, left: 60},
            width = 1280 - margin.left - margin.right,
            height = 500 - margin.top - margin.bottom;

        var x = d3.scale.linear()
            .domain([
                d3.min(data, function (d) {
                    return d["value"][0];
                }) - 0.05,
                d3.max(data, function (d) {
                    return d["value"][0];
                }) + 0.05
            ])
            .range([0, width]);

        var y = d3.scale.linear()
            .domain([0, d3.max(data, function (d) {
                return d["value"][1];
            })])
            .range([height, 0]);

        var chart = d3.select('#tfidf')
            .append('svg:svg')
            .attr('width', width + margin.right + margin.left)
            .attr('height', height + margin.top + margin.bottom)
            .attr('class', 'chart');

        var main = chart.append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
            .attr('width', width)
            .attr('height', height)
            .attr('class', 'main');

        // draw the x axis
        var xAxis = d3.svg.axis()
            .scale(x)
            .orient('bottom');

        main.append('g')
            .attr('transform', 'translate(0,' + height + ')')
            .attr('class', 'main axis date')
            .call(xAxis);

        // draw the y axis
        var yAxis = d3.svg.axis()
            .scale(y)
            .orient('left');

        main.append('g')
            .attr('transform', 'translate(0,0)')
            .attr('class', 'main axis date')
            .call(yAxis);

        var zoom = d3.behavior.zoom()
            .scaleExtent([1, 20])
            .on("zoom", zoomCallback);

        chart.call(zoom);
        var g = main.append("svg:g");

        function zoomCallback() {
            chart.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
        }

        var tooltip = d3.select("body").append("div")
            .attr("class", "tooltip")
            .style("opacity", 0);

        var dots = g.selectAll("scatter-dots")
            .data(data)
            .enter().append("svg:circle")
            .attr("cx", function (d, i) {
                return x(d["value"][0]);
            })
            .attr("cy", function (d) {
                return y(d["value"][1]);
            })
            .attr("r", 4);
        dots
            .on("mouseover", function (d) {
                tooltip
                    .transition()
                    .duration(200)
                    .style("opacity", .9);
                tooltip.html(d.tooltip)
                    .style("left", (d3.event.pageX) + "px")
                    .style("top", (d3.event.pageY - 28) + "px");
            })
            .on("mouseout", function (d) {
                tooltip
                    .transition()
                    .duration(200)
                    .style("opacity", 0)
            });
    }
});

