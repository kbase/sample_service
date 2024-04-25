
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
 * <p>Original spec-file type: ExpireDataLinkParams</p>
 * <pre>
 * expire_data_link parameters.
 *         upa - the workspace upa of the object from which the link originates.
 *         dataid - the dataid, if any, of the data within the object from which the link originates.
 *             Omit for links where the link is from the entire object.
 *         as_admin - run the method as a service administrator. The user must have full
 *             administration permissions.
 *         as_user - expire the link as a different user. Ignored if as_admin is not true. Neither
 *             the administrator nor the impersonated user need have permissions to the link if a
 *             new version is saved.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "upa",
    "dataid",
    "as_admin",
    "as_user"
})
public class ExpireDataLinkParams {

    @JsonProperty("upa")
    private String upa;
    @JsonProperty("dataid")
    private String dataid;
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

    public ExpireDataLinkParams withUpa(String upa) {
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

    public ExpireDataLinkParams withDataid(String dataid) {
        this.dataid = dataid;
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

    public ExpireDataLinkParams withAsAdmin(Long asAdmin) {
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

    public ExpireDataLinkParams withAsUser(String asUser) {
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
        return ((((((((((("ExpireDataLinkParams"+" [upa=")+ upa)+", dataid=")+ dataid)+", asAdmin=")+ asAdmin)+", asUser=")+ asUser)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
