
package us.kbase.sampleservice;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: CreateDataLinkParams</p>
 * <pre>
 * create_data_link parameters.
 *         upa - the workspace UPA of the object to be linked.
 *         dataid - the dataid of the data to be linked, if any, within the object. If omitted the
 *             entire object is linked to the sample.
 *         id - the sample id.
 *         version - the sample version.
 *         node - the sample node.
 *         update - if false (the default), fail if a link already exists from the data unit (the
 *             combination of the UPA and dataid). if true, expire the old link and create the new
 *             link unless the link is already to the requested sample node, in which case the
 *             operation is a no-op.
 *         as_admin - run the method as a service administrator. The user must have full
 *             administration permissions.
 *         as_user - create the link as a different user. Ignored if as_admin is not true. Neither
 *             the administrator nor the impersonated user need have permissions to the data or
 *             sample.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "upa",
    "dataid",
    "id",
    "version",
    "node",
    "update",
    "as_admin",
    "as_user"
})
public class CreateDataLinkParams {

    @JsonProperty("upa")
    private String upa;
    @JsonProperty("dataid")
    private String dataid;
    @JsonProperty("id")
    private String id;
    @JsonProperty("version")
    private Long version;
    @JsonProperty("node")
    private String node;
    @JsonProperty("update")
    private Long update;
    @JsonProperty("as_admin")
    private Long asAdmin;
    @JsonProperty("as_user")
    private String asUser;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("upa")
    public String getUpa() {
        return upa;
    }

    @JsonProperty("upa")
    public void setUpa(String upa) {
        this.upa = upa;
    }

    public CreateDataLinkParams withUpa(String upa) {
        this.upa = upa;
        return this;
    }

    @JsonProperty("dataid")
    public String getDataid() {
        return dataid;
    }

    @JsonProperty("dataid")
    public void setDataid(String dataid) {
        this.dataid = dataid;
    }

    public CreateDataLinkParams withDataid(String dataid) {
        this.dataid = dataid;
        return this;
    }

    @JsonProperty("id")
    public String getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(String id) {
        this.id = id;
    }

    public CreateDataLinkParams withId(String id) {
        this.id = id;
        return this;
    }

    @JsonProperty("version")
    public Long getVersion() {
        return version;
    }

    @JsonProperty("version")
    public void setVersion(Long version) {
        this.version = version;
    }

    public CreateDataLinkParams withVersion(Long version) {
        this.version = version;
        return this;
    }

    @JsonProperty("node")
    public String getNode() {
        return node;
    }

    @JsonProperty("node")
    public void setNode(String node) {
        this.node = node;
    }

    public CreateDataLinkParams withNode(String node) {
        this.node = node;
        return this;
    }

    @JsonProperty("update")
    public Long getUpdate() {
        return update;
    }

    @JsonProperty("update")
    public void setUpdate(Long update) {
        this.update = update;
    }

    public CreateDataLinkParams withUpdate(Long update) {
        this.update = update;
        return this;
    }

    @JsonProperty("as_admin")
    public Long getAsAdmin() {
        return asAdmin;
    }

    @JsonProperty("as_admin")
    public void setAsAdmin(Long asAdmin) {
        this.asAdmin = asAdmin;
    }

    public CreateDataLinkParams withAsAdmin(Long asAdmin) {
        this.asAdmin = asAdmin;
        return this;
    }

    @JsonProperty("as_user")
    public String getAsUser() {
        return asUser;
    }

    @JsonProperty("as_user")
    public void setAsUser(String asUser) {
        this.asUser = asUser;
    }

    public CreateDataLinkParams withAsUser(String asUser) {
        this.asUser = asUser;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((((((((("CreateDataLinkParams"+" [upa=")+ upa)+", dataid=")+ dataid)+", id=")+ id)+", version=")+ version)+", node=")+ node)+", update=")+ update)+", asAdmin=")+ asAdmin)+", asUser=")+ asUser)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
