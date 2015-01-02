%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<p>Current set temperatures</p>
<form action="update" method="get">
<table border="1">
    %for row in rows:
        <tr>
            <td>{{row[1]}}</td>
            <td><input type="text" name="{{row[0]}}" value="{{row[2]}}" size="4" maxlength="4"></td>
        </tr>
    %end
</table>
<input type="submit" name="update" value="Save changes">
</form>
