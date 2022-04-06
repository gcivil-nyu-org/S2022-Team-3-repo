$(document).ready(function() {
    var updatedHtmlClass = "select2-skipme";

    var select2Orginal = $(".select2Control");
    select2Orginal.select2({
        placeholder: 'Select all the applicable categories.'
    });

    var select2Control = $(".select2Control").next();

    var select2UlDesc = select2Control.find("span.select2-selection");
    select2UlDesc.prepend("<span class='sr-only'>Selected Items</span>");

    var searchBoxLi = select2Control.find("li.select2-search");
    var searchBoxInput = select2Control.find("input.select2-search__field");
    if (searchBoxLi) {
        searchBoxLi.attr("role", "search");

        searchBoxLi.addClass(updatedHtmlClass);
        var searchBoxInput = select2Control.find("input.select2-search__field");
        if (searchBoxInput) {
            var searchDescId = select2Orginal.id + "_SearchBox_desc";
            searchBoxInput.attr("aria-describedby", searchDescId);
            searchBoxLi.append("<div id='" + searchDescId + "' class='sr-only'>Optionally you can type to filter and after activating press Up or Down arrows to select or unselect items</div>")
        }
    }
    
        var clearAllSpan = select2Control.find("span.select2-selection__clear");
        if (clearAllSpan) {
            clearAllSpan.text("<i class='fas fa-times' aria-hidden='true'></i><span class='sr-only'>Remove all items</span>");
        }

        var selectUl = select2Control.find("ul.select2-selection__rendered");
        $(selectUl).on('DOMNodeInserted', 'li', function(e) {
            if (e.currentTarget.className.indexOf(updatedHtmlClass) == -1) {
            e.currentTarget.className += " " + updatedHtmlClass;
            var newRemoveItemHtml = "<span aria-hidden='true' class='select2-selection__choice__remove' role='presentation' title='Remove " + e.currentTarget.title + "'><i class='fas fa-times'></i></span>" + e.currentTarget.title;
            if (e.currentTarget.innerHTML.indexOf(updatedHtmlClass) == -1) {
                e.currentTarget.innerHTML = newRemoveItemHtml;
            }
        }
    });

    $('select').on('select2:open', function(e) {
        var dynamixULId = "#" + select2Control.find(".select2-selection").attr("aria-owns");
        $(dynamixULId).on('DOMNodeInserted', 'li', function(e) {
        var currentLi = $(e.currentTarget);

            $(currentLi).attrchange({
                trackValues: true,
                callback: function(event) {
                    if (event.attributeName == "aria-selected") {
                        if (!currentLi.attr("data-select2-data")) {
                        currentLi.attr("data-select2-data", currentLi.text())
                        }
                        currentLi.html("<span class='sr-only'>" +
                        ((event.newValue == "true") ? "Selected" : "") +
                        "</span>" +
                        currentLi.attr("data-select2-data"));
                    }
                }
            });
        });
    });
});
