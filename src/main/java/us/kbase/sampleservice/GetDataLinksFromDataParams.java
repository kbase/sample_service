
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
 * <p>Original spec-file type: GetDataLinksFromDataParams</p>
 * <pre>
 * get_data_links_from_data parameters.
 *         upa - the data UPA.
 *         effective_time - the effective time at which the query should be run - the default is
 *             the current time. Providing a time allows for reproducibility of previous results.
 *         as_admin - run the method as a service administrator. The user must have read
 *             administration permissions.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "upa",
    "effective_time",
    "as_admin"
})
public class GetDataLinksFromDataParams {

    @JsonProperty("upa")
    private String upa;
    @JsonProperty("effective_time")
    private Long effectiveTime;
    @JsonProperty("as_admin")
    private Long asAdmin;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("upa")
    public String getUpa() {
        return upa;
    }

    @JsonProperty("upa")
    public void setUpa(String upa) {
        this.upa = upa;
    }

    public GetDataLinksFromDataParams withUpa(String upa) {
        this.upa = upa;
        return this;
    }

    @JsonProperty("effective_time")
    public Long getEffectiveTime() {
        return effectiveTime;
    }

    @JsonProperty("effective_time")
    public void setEffectiveTime(Long effectiveTime) {
        this.effectiveTime = effectiveTime;
    }

    public GetDataLinksFromDataParams withEffectiveTime(Long effectiveTime) {
        this.effectiveTime = effectiveTime;
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

    public GetDataLinksFromDataParams withAsAdmin(Long asAdmin) {
        this.asAdmin = asAdmin;
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
        return ((((((((("GetDataLinksFromDataParams"+" [upa=")+ upa)+", effectiveTime=")+ effectiveTime)+", asAdmin=")+ asAdmin)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
