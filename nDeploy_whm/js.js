
jQuery(document).ready(function($){

	$(document).ajaxStart(function () {
		$('#loader').show();
	});
	$(document).ajaxStop(function () {
		$('#loader').hide();
	});
	$(document).ajaxError(function () {
		$('#loader').hide();
	});

	$.ajaxSetup({
	    cache: false
	})

    $('[data-toggle="tooltip"]').tooltip();

    $('[data-toggle="popover"]').popover();

    $('#modalForm1').submit(function() {
        var $f = $('#modalForm1');
        var $url = "ddos_mitigate.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal-xl").find('.modal-body').html(result)
            $("#myModal-xl").modal('show');
        }});
    });

    $('#modalForm2').submit(function() {
        var $f = $('#modalForm2');
        var $url = "firehol_control.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal-xl").find('.modal-body').html(result)
            $("#myModal-xl").modal('show');
        }});
    });

    $('#modalForm3').submit(function() {
        var $f = $('#modalForm3');
        var $url = "abnormal_process_detector.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal-nl").find('.modal-body').html(result)
            $("#myModal-nl").modal('show');
        }});
    });

    $('#modalForm4').submit(function() {
        var $f = $('#modalForm4');
        var $url = "fix_unison.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm5').submit(function() {
        var $f = $('#modalForm5');
        var $url = "fix_unison.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm6').submit(function() {
        var $f = $('#modalForm6');
        var $url = "set_default_php.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm7').submit(function() {
        var $f = $('#modalForm7');
        var $url = "sync_gdnsd_zone.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal-nl").find('.modal-body').html(result)
            $("#myModal-nl").modal('show');
        }});
    });

    $('#modalForm8').submit(function() {
        var $f = $('#modalForm8');
        var $url = "save_phpfpm_pool_file.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('.modalForm9-wrap').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        console.log($id);
        var $url = "save_phpfpm_pool_file.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('.modalForm10-wrap').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "save_phpfpm_pool_file.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm11').submit(function() {
        var $f = $('#modalForm11');
        var $url = "save_backup_settings.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm12').submit(function() {
        var $f = $('#modalForm12');
        var $url = "save_borgmatic_settings.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('.modalForm13-wrap').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "save_borgmatic_settings.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm14').submit(function() {
        var $f = $('#modalForm14');
        var $url = "save_borgmatic_settings.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm16').submit(function() {
        var $f = $('#modalForm16');
        var $url = "lock_domain_data_to_package.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm17').submit(function() {
        var $f = $('#modalForm17');
        var $url = "save_pkg_server_settings.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm18').submit(function() {
        var $f = $('#modalForm18');
        var $url = "save_pkg_app_settings.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModalback").find('.modal-body').html(result)
            $("#myModalback").modal('show');
        }});
    });

    $('#modalForm19').submit(function() {
        var $f = $('#modalForm19');
        var $url = "save_resource_limit.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

		$('#modalForm20').submit(function() {
        var $f = $('#modalForm20');
        var $url = "save_phpfpm_pool_file.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#myModal').on('hidden.bs.modal', function () {
    	location.reload()
    });

	$('#myModalback').on('hidden.bs.modal', function () {
		window.history.go(-1);
    });

	$('#myModal-xl').on('hidden.bs.modal', function () {
		location.reload()
	});

});
