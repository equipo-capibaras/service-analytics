function getAuthType() {
  var cc = DataStudioApp.createCommunityConnector();
  var AuthTypes = cc.AuthType;
  return cc
    .newAuthTypeResponse()
    .setAuthType(AuthTypes.NONE)
    .build();
}

function getConfig(request) {
  var cc = DataStudioApp.createCommunityConnector();
  var config = cc.getConfig();

  config.newTextInput()
      .setId('token')
      .setName('token')
      .setAllowOverride(true);

  config.newTextInput()
      .setId('server')
      .setName('server')
      .setAllowOverride(true);

  config.newTextInput()
      .setId('language')
      .setName('language')
      .setAllowOverride(true);

  config.setDateRangeRequired(true);
  config.setIsSteppedConfig(false);
  
  return config.build();
}

function isAdminUser() {
  return true;
}

function getFields(request) {
  var cc = DataStudioApp.createCommunityConnector();
  var fields = cc.getFields();
  var types = cc.FieldType;
  var aggregations = cc.AggregationType;
  
  // Dimensions
  fields.newDimension()
    .setId('userId')
    .setType(types.TEXT);

  fields.newDimension()
    .setId('age')
    .setType(types.TEXT);

  fields.newDimension()
    .setId('language')
    .setType(types.TEXT);

  fields.newDimension()
    .setId('channel')
    .setType(types.TEXT);

  fields.newDimension()
    .setId('country')
    .setType(types.COUNTRY);

  fields.newDimension()
    .setId('product')
    .setType(types.TEXT);

  // Metrics
  fields.newMetric()
    .setId('satisfaction')
    .setType(types.NUMBER)
    .setAggregation(aggregations.AVG);

  return fields;
}

function getSchema(request) {
  var fields = getFields(request).build();
  return { schema: fields };
}

function getData(request) {
  var requestedFieldIds = request.fields.map(function(field) {
    return field.name;
  });
  var requestedFields = getFields().forIds(requestedFieldIds);

  var post_data = {
    'startDate': request.dateRange.startDate,
    'endDate': request.dateRange.endDate,
    'language': request.configParams['language'],
    'fields': requestedFieldIds
  };
  var options = {
    'method' : 'post',
    'contentType': 'application/json',
    'headers': {
      'Authorization': 'Bearer ' + request.configParams['token']
    },
    'payload' : JSON.stringify(post_data)
  };
  var response = UrlFetchApp.fetch('https://' + request.configParams['server'] + '/api/v1/analytics/users', options);
  var response_json = JSON.parse(response);

  return {
    schema: requestedFields.build(),
    rows: response_json.rows
  };
}
