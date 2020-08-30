window.app.config(function ($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/');
    $stateProvider
        .state({
            url: '/tfidf',
            name: 'tfidf',
            controller: 'TfidfController',
            templateUrl: 'web/tfidf/component.html'
        })
        .state({
            url: '/count',
            name: 'count',
            controller: 'CountController',
            templateUrl: 'web/count/component.html'
        })
        .state({
            url: '/',
            name: 'result',
            controller: 'ResultController',
            templateUrl: 'web/result/component.html'
        })
        .state({
            url: '/multilabel',
            name: 'multilabel',
            controller: 'MultiLabelController',
            templateUrl: 'web/multilabel/component.html'
        })
        .state({
            url: '/multiclass',
            name: 'multiclass',
            controller: 'MultiClassController',
            templateUrl: 'web/multiclass/component.html'
        });
});
