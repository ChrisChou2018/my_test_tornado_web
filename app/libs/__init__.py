
def create_html_table(t_heads_data, tbodys_data):
    thead_str = "<thead><tr>"
    for i in t_heads_data:
        thead_str += "<th>{0}</th>".format(i)
    else:
        thead_str += "</tr></thead>"
    tbody_str = "<tbody>"
    for i in tbodys_data:
        tbody_str += "<tr>"
        for j in i:
            tbody_str += "<td>{0}</td>".format(j)
        else:
            tbody_str += "<td><a class='edit_member' style='cursor:pointer;text-decoration:none;'>编辑</a></td> <td style='display: none'><input type='checkbox'></td>"
            tbody_str += "</tr>"
    else:
        tbody_str += "/tbody"
    return thead_str + tbody_str



