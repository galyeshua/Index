var cat_num = 0;
var item_num = 0;

$( function() {
    initMainList();  // make main list sortable
    initCategories();  // add all data from the file, init Item list is inside
});

$( "#addcat" ).on( "click", function() {
    createCategory();
});

function initMainList(){
    $( "#mainList" ).sortable({
        placeholder: "main-ui-highlight",
        items: "> li:not(.ui-state-disabled)",
        scroll: true,
        opacity: 0.9
    });
    $( "#mainList" ).disableSelection();
}

function initItemList(){
    $( ".sortable" ).sortable({
        placeholder: "item-highlight col-xs-6 col-sm-4 col-md-3 col-lg-2",
        connectWith: ".sortable",
        items: "> li:not(.ui-state-disabled, div)",
        opacity: 0.7
    });
    $( ".sortable" ).disableSelection();
}

function initCategories(){
    $.ajax({
      type: "POST",
      url: "json",
      dataType: 'json',
      success: function(data){
        $.each(data['categories'], function(index, cat){
            var cat_name = cat['name'];
            var cat_id = createCategory(cat_name);
            $.each(cat['items'], function(index, item){
                createItem(cat_id, item['name'], item['url'], item['type']);
            })
            //console.log('category "' + cat_name + '" created (' + cat_id + ')');
        })
      }
    });
}

function dataSerialize(){
    var exp_cat_id = 0;
    var total_string='';
    var con_list = [];

    con_list.push('csrf_token='+$('#csrf_token').val());

    var categories_id = $( "#mainList" ).sortable( "toArray" );
    $.each(categories_id, function(index, value){
        var category = 'categories-' + exp_cat_id;
        category_obj = $("#" + value);
        category_name =category + '-name' + '=' + encodeURIComponent(category_obj.find('.category_name').val());
        con_list.push(category_name);

        var exp_item_id = 0;
        var items_id = category_obj.find('.category_items').sortable( "toArray" );
        $.each(items_id, function(index, value){
            var item = category + '-items-' + exp_item_id;
            item_obj = $("#" + value);

            item_name =item + '-name' + '=' + encodeURIComponent(item_obj.find('.item_name').text());
            item_type =item + '-type' + '=' + encodeURIComponent(item_obj.find('.item_type').text());
            item_url =item + '-url' + '=' + encodeURIComponent(item_obj.find('.item_url').text());
            con_list.push(item_name);
            con_list.push(item_type);
            con_list.push(item_url);

            exp_item_id += 1;
        })
        exp_cat_id += 1;
    })

    total_string = con_list.join('&')
    //console.log(total_string);
    return total_string;
}

function verifyAndSave(url){
    data_string = dataSerialize();

    $.ajax({
          type: "POST",
          url: url,
          data: data_string,
          success: function(data){
            //console.log('verified successfully');
            window.location = '/admin';
            //document.getElementById("res").innerHTML = 'SAVED';
            //$('#res').html('<div class="alert alert-success" role="alert">Data Saved successfully</div>');
          },
          error: function(data){
            console.log('ERROR WITH FILE - ' + data.status + '(' + data.statusText + ')');
            $('#res').html('<div class="alert alert-danger" role="alert"><strong>ERROR</strong> ' + data.responseJSON['message'] + '</div>');
            $('#export').removeAttr("disabled");
          }
        }).always(function() {
            //$('#export').removeAttr("disabled");
        });
}

function createCategory(cat_name=''){
    var cat_id = 'category_block' + cat_num;
    cat_num += 1;

    template = $("#templateCategory").clone();
    template.attr("id",cat_id);
    template.find('.category_name').val(cat_name)
    template.find('.category_add').attr("data-cat", cat_id);
    $( "#endlist" ).before(template);

    $("#" + cat_id).find('.category_del').on( "click", function() { deleteObj(cat_id); });

    initItemList();
    return cat_id;
}

function createItem(cat_id, name='', url='', type=''){
    var item_id = 'item_block' + item_num;
    item_num += 1;

    template = $("#templateItem").clone();
    template.attr("id",item_id);
    template.find('.item_name').text(name)
    template.find('.item_url').text(url)
    template.find('.item_type').text(type)
    template.find('.priv').html('<span class="glyphicon glyphicon-' + type + '" aria-hidden="true"></span>')
    template.find('.item_edit').attr("data-item", item_id);
    $( "#" + cat_id ).find('.category_items').append(template);

    $("#" + item_id).find('.item_del').on( "click", function() { deleteObj(item_id); });
    //$("#" + item_id).find('.item_dup').on( "click", function() { createItem(cat_id, name, url, type); });

    return item_id;
}


$('#itemModal').on('show.bs.modal', function (event) {
  $( "#add" ).off( "click" );
  var button = $(event.relatedTarget) // Button that triggered the modal
  var item_id = button.data('item') // Extract info from data-* attributes
  var cat_id = button.data('cat') // Extract info from data-* attributes
  var modal = $(this)

  if (cat_id){
  // CREATE
    modal.find('.modal-title').text('Add New Item')
    modal.find('#item_name').val('')
    modal.find('#item_url').val('')
    modal.find('#item_type').val('globe')

    $( "#add" ).on( "click", function() {
      createItem(cat_id, $("#item_name").val(), $("#item_url").val(), $("#item_type").val());
      $('#itemModal').modal('hide');
      }
    );
  } else if (item_id){
  // EDIT
    modal.find('.modal-title').text('Edit Item')

    modal.find('#item_name').val($("#" + item_id).find('.item_name').text())
    modal.find('#item_url').val($("#" + item_id).find('.item_url').text())
    modal.find('#item_type').val($("#" + item_id).find('.item_type').text())

      $( "#add" ).on( "click", function() {
        $("#" + item_id).find('.item_name').text($('#item_name').val())
        $("#" + item_id).find('.item_url').text($('#item_url').val())
        $("#" + item_id).find('.item_type').text($('#item_type').val())
        $("#" + item_id).find('.priv').html('<span class="glyphicon glyphicon-' + $('#item_type').val() + '" aria-hidden="true"></span>')
        $('#itemModal').modal('hide');}
      );
  }
})

function deleteObj(obj_id){
    if (confirm('Are you sure?')){
       $( "#" + obj_id ).remove();
    }
}