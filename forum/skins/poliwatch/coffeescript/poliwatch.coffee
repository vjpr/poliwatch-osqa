$ ->

  source = [
    {
      value: "http://www.foo.com",
      label: "Spencer Kline"
    },
    {
      value: "http://www.example.com",
      label: "James Bond"
    }
  ]

  ###
  $("input#keywords").autocomplete
    source: source
    select: (event,ui) ->
      console.log ui.item.value
      window.location.href = ui.item.value
    appendTo: 'div'
  ###

  # AUTOCOMPLETE

  data = [
    label: "anders"
    category: ""
  ,
    label: "andreas"
    category: ""
  ,
    label: "antal"
    category: ""
  ,
    label: "Infrastructure"
    category: "Topic"
  ,
    label: "Climate Change"
    category: "Topic"
  ,
    label: "Education"
    category: "Topic"
  ,
    label: "Tony Abbott"
    category: "Politician"
  ,
    label: "Julia Gillard"
    category: "Politician"
  ,
    label: "Penny Wong"
    category: "Politician"
  ]

  #$('<p>Test</p>').appendTo("#search-container")

  $.widget "custom.catcomplete", $.ui.autocomplete,
    _renderMenu: (ul, items) ->
      self = this
      currentCategory = ""
      $.each items, (index, item) ->
        unless item.category == currentCategory
          ul.append "<li class='ui-autocomplete-category'>" + item.category + "</li>"
          currentCategory = item.category
        self._renderItem ul, item
    #appendTo: $("#searchContainer")

  $("#keywords").catcomplete
    delay: 0
    minLength: 0
    source: data
    appendTo: $("#search-container")
    minChars: 0
    open: (event, ui) ->
      $(".ui-autocomplete").css("position", "relative")
      $(".ui-autocomplete").css("top", "0px")
      $(".ui-autocomplete").css("left", "0px")
  .focus ->
    $("#keywords").catcomplete('search','')

  a = 1