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
    .setId('date')
    .setType(types.YEAR_MONTH_DAY);

  fields.newDimension()
    .setId('hour')
    .setType(types.HOUR);

  fields.newDimension()
    .setId('channel')
    .setType(types.TEXT);
  
  fields.newDimension()
    .setId('risk')
    .setType(types.TEXT);

  fields.newDimension()
    .setId('product_name')
    .setType(types.TEXT);

  fields.newDimension()
    .setId('agent_name')
    .setType(types.TEXT);

  // Metrics
  fields.newMetric()
    .setId('escalations')
    .setType(types.NUMBER)
    .setAggregation(aggregations.AVG);

  fields.newMetric()
    .setId('resolution_time')
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
    'endDate': request.dateRange.startDate,
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
  var response = UrlFetchApp.fetch('https://' + request.configParams['server'] + '/api/v1/analytics/incidents', options);
  var response_json = JSON.parse(response);

  return {
    schema: requestedFields.build(),
    rows: response_json.rows
  };
}
