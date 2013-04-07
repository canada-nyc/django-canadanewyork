(function () {

var records = {};

CANADA.store = {

  /**
    Load a record into the store of the given
    record type.

    @method load
    @param recordType {String}
    @param json {Object} The JSON representation of the object,
      which **must** have an `id` attribute on it.
   */
  load: function (recordType, json) {
    if (!json.hasOwnProperty('id')) {
      throw new TypeError("A record **must** have an `id` attribute.");
    }

    if (typeof records[recordType] === "undefined") {
      records[recordType] = {};
    }

    records[recordType][json.id] = json;
  },

  /**
    Returns the record with the given id.

    @method load
    @param recordType {String}
    @param id {String} The id of the record to be found.
   */
  find: function (recordType, id) {
    return records[recordType][id];
  }
};

}());
