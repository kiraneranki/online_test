$(document).ready(function(){
    /* selectors for the 3 step tabs*/
    $fixed_tab = $("#fixed-tab");
    $random_tab = $("#random-tab");
    $finish_tab = $("#finish-tab");

    $question_type = $("#id_question_type");
    $marks = $("#id_marks");

    /* ajax requsts on selectors change */
    $question_type.change(function() {
        $.ajax({
            url: "/exam/ajax/questionpaper/marks/",
            type: "POST",
            data: {
                question_type: $question_type.val()
            },
            dataType: "html",
            success: function(output) {
                $marks.html(output);
            }
        });
    });

    $marks.change(function() {
        $.ajax({
            url: "/exam/ajax/questionpaper/questions/",
            type: "POST",
            data: {
                question_type: $question_type.val(),
                marks: $marks.val()
            },
            dataType: "html",
            success: function(output) {
                if($fixed_tab.hasClass("active")) {
                    var questions = $(output).filter("#questions").html();
                    $("#fixed-available").html(questions);
                } else if($random_tab.hasClass("active")) {
                    var questions = $(output).filter("#questions").html();
                    var numbers = $(output).filter("#num").html();
                    $("#random-available").html(questions);
                    $("#number-wrapper").html(numbers);
                }
            }
        });
    });

    /* adding fixed questions */
    $("#add-fixed").click(function(e) {
        var count = 0;
        var selected = [];
        var html = "";
        var $element;
        $("#fixed-available input:checkbox").each(function(index, element) {
            if($(this).attr("checked")) {
                qid = $(this).attr("data-qid");
                selected.push(qid);
                $element = $("<div class='qcard'></div>");
                html += "<li>" + $(this).next().html() + "</li>";
                count++;
            }
        });
        html = "<ul>" + html + "</ul>";
        selected = selected.join(",");
        var $input = $("<input type='hidden'>");
        $input.attr({
            value: selected,
            name: "fixed"
        });
        $remove = $("<a href='#' class='remove'>&times;</div>");
        $element.html(count + " questions added").append(html).append($input).append($remove);
        $("#fixed-added").prepend($element);
    e.preventDefault();
    });

    /* adding random questions */
    $("#add-random").click(function(e) {
        $numbers = $("#numbers");
        console.log($numbers.val());
        if($numbers.val()) {
            $numbers.removeClass("red-alert");
            var count = 0;
            var selected = [];
            var html = "";
            var $element;
            $("#random-available input:checkbox").each(function(index, element) {
                if($(this).attr("checked")) {
                    qid = $(this).attr("data-qid");
                    selected.push(qid);
                    $element = $("<div class='qcard'></div>");
                    html += "<li>" + $(this).next().html() + "</li>";
                    count++;
                }
            });
            html = "<ul>" + html + "</ul>";
            selected = selected.join(",");
            var $input_random = $("<input type='hidden'>");
            $input_random.attr({
                value: selected,
                name: "random"
            });
            var $input_number = $("<input type='hidden'>");
            $input_number.attr({
                value: $numbers.val(),
                name: "number"
            });
            $remove = $("<a href='#' class='remove'>&times;</div>");
            $element.html(count + " questions added").append(html).append($input_random).append($input_number).append($remove);
            $("#random-added").prepend($element);
        } else {
            $numbers.addClass("red-alert");
        }
    e.preventDefault();
    });

    /* removing added questions */
    $(".qcard .remove").live("click", function(e) {
        $(this).parent().slideUp("normal", function(){ $(this).remove(); });
    e.preventDefault();
    });

    /* showing/hiding selectors on tab click */
    $(".tabs li").click(function() {
        if($(this).attr("id") == "finish-tab") {
            $("#selectors").hide();
        } else {
            $("#selectors").show();
        }
    });
}); //document
