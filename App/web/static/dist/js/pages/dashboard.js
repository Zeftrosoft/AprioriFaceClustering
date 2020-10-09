var invoice_data =[]
var predict_data = []
var current_lid = ''
var montage_data = []
var invoiceListId = "#InvoiceList"
var invoiceItemListId = "#InvoiceItemlist"
var predictionListId = "#PredictionList"
var allPredictionListId = "#AllPrediction"
var invoiceNoId = "#InvoiceNo"
var invoiceImageId = "#InvoiceImage"

var minimum_Support = 0.2
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
          initInvoices(id)
        }
    },
    error: function (data) {
        console.log("Error While Getting Invoice Data");
        console.log(data);
    }
  });
}

function initInvoices(invId) {
  console.log('invoice Data')
  
  $(invoiceListId+'-'+invId).html('')
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
        
        console.log();
        fillPredictionList(JSON.parse(predict_data), id)
        }
    },
    error: function (data) {
        console.log("Error While Getting Prediction Data");
        console.log(data);
    }
  });
}

function getAllPredictionData(){
  $.ajax({
    cache: false,
    type: 'GET',
    url:   getPredictDataUrl()+'/all',
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
        
        console.log();
        fillAllPredictionList(JSON.parse(predict_data))
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
function predictAll(){
  getAllPredictionData()
}

function fillPredictionList(predictions, current_lid) {
  var list = []
  console.log(predictions[0]);
  var pred_list = $.grep(predictions, function (row, indx) {
    //console.log(row.support, row.support >= 0.1);
    return row.support >= minimum_Support
  })
  pred_list = pred_list.sort(function (a, b) { return b.support - a.support})
  console.log(pred_list[0]);
  // image_path=$('#InvoiceImage').prop('src', invItems[0][0]);
  // console.log(image_path)
  $.each(pred_list, function (indx, row) {
    var items = row.itemsets.reduce(function (sum, x, i) {
      return sum = sum + ', ' +x
    })
    items = items+' | Support: '+row.support
    var html = `
      <li class="nav-item" style="border-bottom: 1px solid #dfdfdf">
        <a href="#" class="nav-link" style="color:red">
          ${(items)}
        </a>
      </li>
    `             
    list.push(html)   
  })
 console.log('Current LId',current_lid);
  
  $(predictionListId+'-'+current_lid).html(list)
}
function fillAllPredictionList(predictions) {
  var list = []
  console.log(predictions[0]);
  var pred_list = $.grep(predictions, function (row, indx) {
    //console.log(row.support, row.support >= 0.1);
    return row.support >= minimum_Support
  })
  pred_list = pred_list.sort(function (a, b) { return b.support - a.support})
  console.log(pred_list[0]);
  // image_path=$('#InvoiceImage').prop('src', invItems[0][0]);
  // console.log(image_path)
  $.each(pred_list, function (indx, row) {
    var items = row.itemsets.reduce(function (sum, x, i) {
      return sum = sum + ', ' +x
    })
    items = items+' | Support: '+row.support
    var html = `
      <li class="nav-item" style="border-bottom: 1px solid #dfdfdf">
        <a href="#" class="nav-link" style="color:red">
          ${(items)}
        </a>
      </li>
    `             
    list.push(html)   
  })
  
  $(allPredictionListId).html(list)
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
          console.error('Serverside Error While Getting Montage Data');
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

