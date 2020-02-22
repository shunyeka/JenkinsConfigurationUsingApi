class JobManager {
  constructor() {
    this.init();
    this.initEvents();
  }
  init() {
    //Load all job
    this.loadAll(this);
  }
  initEvents() {
    var self = this;
    //Add new job
    $(document).on('click', '#create-new-job', function(e) {
      e.preventDefault();
      self.createJob();
    });
    //Build a job
    $(document).on('click', '.build', function(e) {
      self.buildJob($(this));
    });
    //Delete a job
    $(document).on('click', '.delete', function(e) {
      self.deleteJob($(this));
    });
  }
  loadAll(self) {
    $('body').removeClass('modal-open');
    $.ajax({
      url: 'http://127.0.0.1:5000/jobs',
      type: 'GET',
      crossDomain: true,
      dataType: "json",
      contentType: 'application/json',
    }).done(function(jsonObj) {
      console.log(jsonObj)
      self.addRows(jsonObj);
    }).fail(function(msg) {
      alert(JSON.stringify(msg));
    });
  }
  createJob() {
    $('#new-job-modal').modal('show');
    $('#new-job-form').on('submit', function(e) {
      e.preventDefault();
      let create_data = {
        'name': $('#new-job-name').val(),
        'description': $('#new-job-description').val(),
        'project_type': $('#new-job-type').val(),
        'url': $('#new-job-url').val(),
      };
      $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:5000/jobs',
        crossDomain: true,
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(create_data)
      }).done(function(jsonObj) {
        self.addRows(jsonObj);
        $('#new-job-modal').modal('hide');
      }).fail(function(error) {
        $('#new-job-modal').modal('hide');
        alert(JSON.stringify(error));
      });
    });
  }
  buildJob(self) {
    $.ajax({
      type: 'POST',
      url: 'http://127.0.0.1:5000/builds',
      crossDomain: true,
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ 'name': self.parent().siblings('.job-name').text() }),
    }).done(function(jsonObj) {
      console.log(jsonObj);
    }).fail(function(error) {
      alert(JSON.stringify(error));
    });
  }
  deleteJob(self) {
    $.ajax({
      type: 'DELETE',
      url: 'http://127.0.0.1:5000/jobs',
      crossDomain: true,
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ 'name': self.parent().siblings('.job-name').text() }),
    }).done(function(jsonObj) {
      self.parent().parent().remove();
      console.log(jsonObj);
    }).fail(function(error) {
      alert(JSON.stringify(error));
    });
  }
  addRows(jsonObj) {
    var markup = '';
    $.each(jsonObj, function(i, obj) {
      markup += "<tr>" + "<td class='job-name'>" + obj.name + "</td>" + "<td class='job-url'>" + obj.url + "</td>" + "<td><button class='build btn text-white' style='background-color:" + obj.color + ";'>Build</button></td>" + "<td><button class='delete btn text-white' style='background-color:" + obj.color + ";'>Delete</button></td>" + "</tr>";
    });
    $('#user-table').append(markup);
  }
}
$(document).ready(function() {
  var jobManager = new JobManager();
});