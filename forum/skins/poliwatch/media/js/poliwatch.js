(function() {
  $(function() {
    var a, data, source;
    source = [
      {
        value: "http://www.foo.com",
        label: "Spencer Kline"
      }, {
        value: "http://www.example.com",
        label: "James Bond"
      }
    ];
    /*
    $("input#keywords").autocomplete
      source: source
      select: (event,ui) ->
        console.log ui.item.value
        window.location.href = ui.item.value
      appendTo: 'div'
    */
    data = [
      {
        label: "anders",
        category: ""
      }, {
        label: "andreas",
        category: ""
      }, {
        label: "antal",
        category: ""
      }, {
        label: "Infrastructure",
        category: "Topic"
      }, {
        label: "Climate Change",
        category: "Topic"
      }, {
        label: "Education",
        category: "Topic"
      }, {
        label: "Tony Abbott",
        category: "Politician"
      }, {
        label: "Julia Gillard",
        category: "Politician"
      }, {
        label: "Penny Wong",
        category: "Politician"
      }
    ];
    $.widget("custom.catcomplete", $.ui.autocomplete, {
      _renderMenu: function(ul, items) {
        var currentCategory, self;
        self = this;
        currentCategory = "";
        return $.each(items, function(index, item) {
          if (item.category !== currentCategory) {
            ul.append("<li class='ui-autocomplete-category'>" + item.category + "</li>");
            currentCategory = item.category;
          }
          return self._renderItem(ul, item);
        });
      }
    });
    $("#keywords").catcomplete({
      delay: 0,
      minLength: 0,
      source: data,
      appendTo: $("#search-container"),
      minChars: 0,
      open: function(event, ui) {
        $(".ui-autocomplete").css("position", "relative");
        $(".ui-autocomplete").css("top", "0px");
        return $(".ui-autocomplete").css("left", "0px");
      }
    }).focus(function() {
      return $("#keywords").catcomplete('search', '');
    });
    return a = 1;
  });
}).call(this);
