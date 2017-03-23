/**
 * Created by XXW on 2017/3/23.
 */
$(".a-upload").on("change","input[type='file']",function(){
    var filePath=$(this).val();
    if(filePath.indexOf("jpg")!=-1 || filePath.indexOf("png")!=-1){
        $(".fileerrorTip").html("").hide();
        var arr=filePath.split('\\');
        var fileName=arr[arr.length-1];
        $(".showFileName").html(fileName);
    }else{
        $(".showFileName").html("");
        $(".fileerrorTip").html("您未上传文件，或者您上传文件类型有误！").show();
        return false
    }
})

function fileChange(target) {
     var fileSize = 0;
     if (isIE && !target.files) {
       var filePath = target.value;
       var fileSystem = new ActiveXObject("Scripting.FileSystemObject");
       var file = fileSystem.GetFile (filePath);
       fileSize = file.Size;
     } else {
      fileSize = target.files[0].size;
      }
      var size = fileSize / 1024;
      if(size>2000){
       alert("附件不能大于2M");
       target.value="";
       return
      }
      var name=target.value;
      var fileName = name.substring(name.lastIndexOf(".")+1).toLowerCase();
      if(fileName !="xls" && fileName !="xlsx"){
          alert("请选择execl格式文件上传！");
          target.value="";
          return
      }
    }

   function filefujianChange(target) {
       var fileSize = 0;
       if (isIE && !target.files) {
         var filePath = target.value;
         var fileSystem = new ActiveXObject("Scripting.FileSystemObject");
         var file = fileSystem.GetFile (filePath);
         fileSize = file.Size;
       } else {
        fileSize = target.files[0].size;
        }
        var size = fileSize / 1024;
        if(size>2000){
         alert("附件不能大于2M");
         target.value="";
         return
        }
        var name=target.value;
        var fileName = name.substring(name.lastIndexOf(".")+1).toLowerCase();
        if(fileName !="jpg" && fileName !="jpeg" && fileName !="pdf" && fileName !="png" && fileName !="dwg" && fileName !="gif" ){
          alert("请选择图片格式文件上传(jpg,png,gif,dwg,pdf,gif等)！");
            target.value="";
            return
        }
      }