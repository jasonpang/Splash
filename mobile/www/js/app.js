var splashapp = angular.module('splash-app', ['ui.bootstrap']);

splashapp.config(['$httpProvider', function ($httpProvider) {

    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
}]);

splashapp.controller('MainCtrl', function ($rootScope, $scope, $http) {
    $rootScope.serverUrl = 'http://white.jasonpang.org:5000';

    $scope.save = function () {
        $http({
            method: 'GET',
            url: $rootScope.serverUrl + '/users',
            data: ''}).
            success(function (data, status, headers, config) {
                $scope.users = data.response;
            }).get()
            error(function (data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
            });
        alert($scope.users)
    };
});