// $(function() {
// 	//If check_all checked then check all table rows
// 	$("#checkAll").on("click", function () {
// 		if ($("input:radio").prop("checked")) {
// 			$("input:radio[id='0']").prop("checked", true);
// 		} else {
// 			$("input:radio[id='0']").prop("checked", false);
// 		}
// 	});

// 	// Check each table row checkbox
// 	$("input:radio[id='0']").on("change", function () {
// 		var total_check_boxes = $("input:radio[id='0']").length;
// 		var total_checked_boxes = $("input:radio[id='0']:checked").length;

// 		// If all checked manually then check check_all checkbox
// 		if (total_check_boxes === total_checked_boxes) {
// 			$("#checkAll").prop("checked", true);
// 		}
// 		else {
// 			$("#checkAll").prop("checked", false);
// 		}
// 	});

//     //If check_all checked then check all table rows
// 	$("#checkAll").on("click", function () {
// 		if ($("input:radio").prop("checked")) {
// 			$("input:radio[id='1']").prop("checked", true);
// 		} else {
// 			$("input:radio[id='1']").prop("checked", false);
// 		}
// 	});

// 	// Check each table row checkbox
// 	$("input:radio[id='0']").on("change", function () {
// 		var total_check_boxes = $("input:radio[id='1']").length;
// 		var total_checked_boxes = $("input:radio[id='1']:checked").length;

// 		// If all checked manually then check check_all checkbox
// 		if (total_check_boxes === total_checked_boxes) {
// 			$("#checkAll").prop("checked", true);
// 		}
// 		else {
// 			$("#checkAll").prop("checked", false);
// 		}
// 	});

//     //If check_all checked then check all table rows
// 	$("#checkAll").on("click", function () {
// 		if ($("input:radio").prop("checked")) {
// 			$("input:radio[id='NA']").prop("checked", true);
// 		} else {
// 			$("input:radio[id='NA']").prop("checked", false);
// 		}
// 	});

// 	// Check each table row checkbox
// 	$("input:radio[id='0']").on("change", function () {
// 		var total_check_boxes = $("input:radio[id='NA']").length;
// 		var total_checked_boxes = $("input:radio[id='NA']:checked").length;

// 		// If all checked manually then check check_all checkbox
// 		if (total_check_boxes === total_checked_boxes) {
// 			$("#checkAll").prop("checked", true);
// 		}
// 		else {
// 			$("#checkAll").prop("checked", false);
// 		}
// 	});
// });

// // var btns = document.querySelectorAll('input[type="radio"]')
// // for (var i=0; i<btns.length; i++){
// //     if(btns[i].id=="0")
// //     btns[i].checked=true;
// // }