/*! Remote 1.0.0 - MIT license - Copyright 2024 Deivid Hugo */
/*! Modified by Deivid Hugo to RemoteInDjangoForm */

(function($) {
    "use strict";

    $.remoteInDjangoForm = function(options) {
        var defaults = $.fn.remoteInDjangoForm.defaults;
        var settings = $.extend({}, defaults, options);

        function updateOptions(data) {
            var selectedValue = selectElement.val() || '';

            selectElement.empty();

            var options = [];

            if (settings.emptyLabel) {
                options.push(['', settings.emptyLabel]);
            }

            if ($.isArray(data)) {
                options = $.isArray(data[0]) ? options.concat(data) : options.concat($.map(data, function(item) {
                    return $.map(item, function(value, key) {
                        return [[key, value]];
                    });
                }));
            } else {
                for (var key in data) {
                    if (data.hasOwnProperty(key)) {
                        options.push([key, data[key]]);
                    }
                }
            }

            for (var i = 0; i < options.length; i++) {
                var key = options[i][0];
                var value = options[i][1];

                var option = $("<option />").val(key).text(value);
                selectElement.append(option);
            }

            if (selectedValue) {
                selectElement.val(selectedValue);
            }

            selectElement.prop("disabled", options.length === 0);
            selectElement.trigger("change");
        }

        function fetchData() {
            if (!settings.url) {
                console.error("RemoteInDjangoForm error: URL not specified.");
                return;
            }

            $.getJSON(settings.url, function(responseData) {
                updateOptions(responseData);
            });
        }

        var selectElement = $(this);

        if (settings.bootstrap) {
            updateOptions(settings.bootstrap);
        }

        fetchData(); 
        return selectElement;
    };

    $.fn.remoteInDjangoForm = $.remoteInDjangoForm;

    $.fn.remoteInDjangoForm.defaults = {
        bootstrap: null,
        emptyLabel: null, 
    };
})(window.jQuery || window.Zepto);


function applyRemoteInDjangoForm($targetElement) {
    $targetElement.remoteInDjangoForm({
        url: $targetElement.data('url'),
        emptyLabel: $targetElement.data('empty-label') === '' ? null : $targetElement.data('empty-label'),
    });
}

function initializeRemoteInDjangoForms() {
    $('.remote-in-django-form').filter(function() {
        return !$(this).attr('name')?.includes('__prefix__');
    }).each(function() {
        applyRemoteInDjangoForm($(this));
    });
    
}

/*! Chained 1.0.0 - MIT license - Copyright 2010-2014 Mika Tuupola */
/*! Modified by Deivid Hugo */

(function($) {
    "use strict";

    $.fn.remoteChainedInDjangoForm = function(options) {
        var defaults = $.fn.remoteChained.defaults;
        var settings = $.extend({}, defaults, options);

        if (settings.loading) {
            settings.clear = true;
        }

        return this.each(function() {
            function updateOptions(data) {
                var selectedValue = $(":selected", selectElement).val();
                $("option", selectElement).remove();
                var options = [];

                if (settings.emptyLabel) {
                    options.push(['', settings.emptyLabel]);
                }

                if ($.isArray(data)) {
                    options = $.isArray(data[0]) ? options.concat(data) : options.concat($.map(data, function(item) {
                        return $.map(item, function(value, key) {
                            return [[key, value]];
                        });
                    }));
                } else {
                    for (var key in data) {
                        if (data.hasOwnProperty(key)) {
                            options.push([key, data[key]]);
                        }
                    }
                }

                for (var i = 0; i < options.length; i++) {
                    var key = options[i][0];
                    var value = options[i][1];

                    if (key !== "selected") {
                        var option = $("<option />").val(key).append(value);
                        $(selectElement).append(option);
                    } else {
                        selectedValue = value;
                    }
                }

                $(selectElement).children().each(function() {
                    if ($(this).val() === selectedValue + "") {
                        $(this).attr("selected", "selected");
                    }
                });

                $(selectElement).trigger("change");
            }

            var selectElement = this;
            var xhr = false;

            $(settings.parents).each(function() {
                $(this).on("change", function() {
                    var requestData = {};

                    $(settings.parents).each(function() {
                        var attributeName = settings.urlParamField !== null ? settings.urlParamField : $(this).attr(settings.attribute);
                        var attributeValue = $(this).is("select") ? $(":selected", this).val() : $(this).val();
                        requestData[attributeName] = attributeValue;

                        if (settings.depends) {
                            $(settings.depends).each(function() {
                                if (selectElement !== this) {
                                    var attributeName = settings.urlParamField !== null ? settings.urlParamField : $(this).attr(settings.attribute);
                                    var attributeValue = $(this).val();
                                    requestData[attributeName] = attributeValue;
                                }
                            });
                        }
                    });

                    if (xhr && $.isFunction(xhr.abort)) {
                        xhr.abort();
                        xhr = false;
                    }

                    if ($(this).val() === "") {
                        updateOptions({});
                        return;
                    }

                    if (settings.clear) {
                        if (settings.loading) {
                            updateOptions.call(selectElement, { "": settings.loading });
                        } else {
                            $("option", selectElement).remove();
                            $(selectElement).trigger("change");
                        }
                    }

                    xhr = $.getJSON(settings.url, requestData, function(responseData) {
                        updateOptions.call(selectElement, responseData);
                    });
                });

                if (settings.bootstrap) {
                    updateOptions.call(selectElement, settings.bootstrap);
                    settings.bootstrap = null;
                }
            });
        });
    };

    $.fn.remoteChainedTo = $.fn.remoteChained;

    $.fn.remoteChained.defaults = {
        attribute: "name",
        urlParamField: null,
        depends: null,
        bootstrap: null,
        loading: null,
        clear: false,
        emptyLabel: null, 
    };
})(window.jQuery || window.Zepto);

function applyRemoteChainedInDjangoForm($targetElement) {
    const parentName = $targetElement.data('parent-name');
    const elementName = $targetElement.attr('name');
    const prefix = elementName.split('-').slice(0, -1).join('-');
    const parentInputId = prefix ? 'id_' + prefix + '-' + parentName : 'id_' + parentName;

    $targetElement.remoteChainedInDjangoForm({
        parents: '#' + parentInputId,
        url: $targetElement.data('url'),
        emptyLabel: $targetElement.data('empty-label') === '' ? null : $targetElement.data('empty-label'),
        urlParamField: $targetElement.data('url-param-field') === '' ? null : $targetElement.data('url-param-field'),
    });

    $('#' + parentInputId).not('.remote-in-django-form').trigger('change');
}

function initializeRemoteChainedInDjangoForms() {
    $('.remote-chained-in-django-form').filter(function() {
        return !$(this).attr('name').includes('__prefix__');
    }).each(function() {
        applyRemoteChainedInDjangoForm($(this));
    });
}

/*! RemoteInDjangoForm 0.1.0 - MIT license - Copyright 2024 Deivid Hugo */

function observeRemoteInDjangoFormsChanges() {
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                const addedNodes = Array.from(mutation.addedNodes).filter(node => node.nodeType === Node.ELEMENT_NODE);
                
                addedNodes.forEach(node => {
                    if (node.matches('.remote-in-django-form, .remote-chained-in-django-form') ||
                        node.querySelector('.remote-in-django-form, .remote-chained-in-django-form')) {
                        
                        const $newElements = $(node).find('.remote-in-django-form, .remote-chained-in-django-form');
                        $newElements.each(function() {
                            if ($(this).hasClass('remote-in-django-form')) {
                                applyRemoteInDjangoForm($(this));
                            }
                            if ($(this).hasClass('remote-chained-in-django-form')) {
                                applyRemoteChainedInDjangoForm($(this));
                            }
                        });
                    }
                });
            }
        });
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

$(document).ready(function() {
    $(window).on('load', function() {
        initializeRemoteInDjangoForms();
        initializeRemoteChainedInDjangoForms();
        observeRemoteInDjangoFormsChanges();
    });
});
