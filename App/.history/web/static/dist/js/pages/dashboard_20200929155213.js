var invoice_data =[]
var predict_data = []
var current_lid = ''
var montage_data = []
var invoiceListId = "#InvoiceList"
var invoiceItemListId = "#InvoiceItemlist"
var invoiceNoId = "#InvoiceNo"
var invoiceImageId = "#InvoiceImage"

$(function () {
  $(document).on('click', '[data-toggle="lightbox"]', function(event) {
    event.preventDefault();
    $(this).ekkoLightbox({
      alwaysShowClose: true
    });
  });
  
})


function  getInvoiceDataUrl() {
  return used_host + '/invoices'
}

function getInvoiceData(id){
  current_lid = id
  $.ajax({
    cache: false,
    type: 'GET',
    url:  getInvoiceDataUrl()+'/'+id,
    xhrFields: {
        // The 'xhrFields' property sets additional fields on the XMLHttpRequest.
        // This can be used to set the 'withCredentials' property.
        // Set the value to 'true' if you'd like to pass cookies to the server.
        // If this is enabled, your server must respond with the header
        // 'Access-Control-Allow-Credentials: true'.
        withCredentials: false
    },
    success: function (json) {
        if (!json.status) {
          console.error('Serverside Error While Geting Invoice Data');
          console.error(json.msg)
        }
        else {
          invoice_data = json.data
          initInvoices()
        }
    },
    error: function (data) {
        console.log("Error While Getting Invoice Data");
        console.log(data);
    }
  });
}

function initInvoices() {
  console.log('invoice Data')
  
  $(invoiceListId+'-0').html('')
  var invoices = invoice_data.map(function (inv) {
    return inv[1]
  })
  var uniq_invs = invoices.filter((v,i,a)=>a.indexOf(v)==i)
 
  
  $.each(uniq_invs, function (indx, row) {
    var html = `
    <li class="nav-item active">
      <a class="nav-link" href="#" onclick="invoiceclicked('${row}')">
        ${row}
      </a>
    </li>
    `             
    $(invoiceListId+'-'+current_lid).append(html)

  })
}

function invoiceclicked(invNo){
  var list = []
  var invItems = $.grep(invoice_data, function (row, indx) {
    return row[1] == invNo
  })
  // image_path=$('#InvoiceImage').prop('src', invItems[0][0]);
  // console.log(image_path)
  $.each(invItems, function (indx, row) {
    var html = `
      <li class="nav-item" style="border-bottom: 1px solid #dfdfdf">
        <a href="#" class="nav-link" style="color:red">
          ${(row[2])}
        </a>
      </li>
    `             
    list.push(html)   
  })
 
  
  $(invoiceItemListId+'-'+current_lid).html(list)
  $(invoiceNoId+'-'+current_lid).html(invNo)
  $(invoiceImageId+'-'+current_lid).html('#InvoiceImage').prop('src', invItems[0][0])
}

function  getPredictDataUrl() {
  return used_host + '/prediction'
}

function getPredictData(id){
  current_lid = id
  console.log( current_lid)
  $.ajax({
    cache: false,
    type: 'GET',
    url:   getPredictDataUrl()+'/'+id,
    xhrFields: {
        // The 'xhrFields' property sets additional fields on the XMLHttpRequest.
        // This can be used to set the 'withCredentials' property.
        // Set the value to 'true' if you'd like to pass cookies to the server.
        // If this is enabled, your server must respond with the header
        // 'Access-Control-Allow-Credentials: true'.
        withCredentials: false
    },
    success: function (json) {
        if (!json.status) {
          console.error('Serverside Error While Geting Prediction Data');
          console.error(json.msg)
        }
        else {
        predict_data = json.data
        
        console.log(JSON.parse(predict_data));
        }
    },
    error: function (data) {
        console.log("Error While Getting Prediction Data");
        console.log(data);
    }
  });
}

function prediction(lid){
  getPredictData(lid)
}


function  getClusterDataUrl() {
  return used_host + '/startclustering'
}

function getClustertData(){
  $.ajax({
    cache: false,
    type: 'GET',
    url:  getClusterDataUrl(),
    xhrFields: {
        // The 'xhrFields' property sets additional fields on the XMLHttpRequest.
        // This can be used to set the 'withCredentials' property.
        // Set the value to 'true' if you'd like to pass cookies to the server.
        // If this is enabled, your server must respond with the header
        // 'Access-Control-Allow-Credentials: true'.
        withCredentials: false
    },
    success: function (json) {
        if (!json.status) {
          console.error('Serverside Error While Geting Montage Data');
          console.error(json.msg)
        }
        else {
          montage_data= json.data
          console.log(montage_data)
        }
    },
    error: function (data) {
        console.log("Error While Getting Montage Data");
        console.log(data);
    }
  });
}
function clustering(){
  getClustertData()
}

