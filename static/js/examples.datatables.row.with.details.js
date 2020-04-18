
(function( $ ) {

	'use strict';

	var datatableInit = function() {
		var $table = $('#datatable-details');
		// format function for row details
		var fnFormatDetails = function( datatable, tr ) {
			var data = datatable.fnGetData( tr );
			var ISBN = data[4];
			// console.log(ISBN);
			var result_data = new Array();
			var tmp_data = new Array();
			for(var i = 0, j = 0; i < book_data.length; i++){
				if (book_data[i][0] == data[4]) {
					tmp_data[j] = book_data[i];
					j++;
				}
			}
			console.log(tmp_data);
			for (var i = 0, j = 0; i < tmp_data.length; i++){
				result_data[j] = '<tr>';
				result_data[j+1] = '<td>' + tmp_data[i][1] + '</td>';
				result_data[j+2] = '<td>' + tmp_data[i][2] + '</td>';
				if (tmp_data[i][6]!=null)
					result_data[j+3] = '<td>' + tmp_data[i][3] + '-' + tmp_data[i][6] + '归还' + '</td>';
				else
					result_data[j+3] = '<td>' + tmp_data[i][3] + '</td>';
				result_data[j+4] = '<tr>';
				j+=5;
			}
			return [
				'<table class="table table-bordered table-striped mb-none">',
					'<thead>',
					'<tr>',
						'<th>条码号</th>',
						'<th>馆藏地</th>',
						'<th>书刊状态</th>',
					'</tr>',
					'</thead>',
					result_data,
				'</div>',

				'<table class="table mb-none">',
				'<tr class="b-top-none">',
					'<td><label class="mb-none">学科主题:</label></td>',
					'<td>' + tmp_data[0][4] + '</td>',
				'</tr>',
				'<tr>',
					'<td><label class="mb-none">提要文摘附注:</label></td>',
					'<td>' + tmp_data[0][5] + '</td>',
				'</tr>',
				'</div>'
			].join('');
		};

		// insert the expand/collapse column
		var th = document.createElement( 'th' );
		var td = document.createElement( 'td' );
		td.innerHTML = '<i data-toggle class="fa fa-plus-square-o text-primary h5 m-none" style="cursor: pointer;"></i>';
		td.className = "text-center";

		$table
			.find( 'thead tr' ).each(function() {
				this.insertBefore( th, this.childNodes[0] );
			});

		$table
			.find( 'tbody tr' ).each(function() {
				this.insertBefore(  td.cloneNode( true ), this.childNodes[0] );
			});

		// initialize
		var datatable = $table.dataTable({
			aoColumnDefs: [{
				bSortable: false,
				aTargets: [ 0 ]
			}],
			aaSorting: [
				[1, 'asc']
			]
		});

		// add a listener
		$table.on('click', 'i[data-toggle]', function() {
			var $this = $(this),
				tr = $(this).closest( 'tr' ).get(0);

			if ( datatable.fnIsOpen(tr) ) {
				$this.removeClass( 'fa-minus-square-o' ).addClass( 'fa-plus-square-o' );
				datatable.fnClose( tr );
			} else {
				$this.removeClass( 'fa-plus-square-o' ).addClass( 'fa-minus-square-o' );
				datatable.fnOpen( tr, fnFormatDetails( datatable, tr), 'details' );
			}
		});
	};

	$(function() {
		datatableInit();
	});

}).apply( this, [ jQuery ]);
